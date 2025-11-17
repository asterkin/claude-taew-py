"""
Context7 API client for documentation queries.

This module provides direct API access to Context7 documentation service,
enabling token-efficient documentation queries through code execution.

Uses Python 3.12+ stdlib only (urllib, tomllib) - no external dependencies.

See ADR-0003 for architectural rationale.
"""

import os
import json
import tomllib
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError


BASE_URL = "https://context7.com/api/v1"
API_KEY = os.getenv("CONTEXT7_API_KEY")


class Context7Error(Exception):
    """Base exception for Context7 API errors."""
    pass


class Context7AuthError(Context7Error):
    """Authentication error (401)."""
    pass


class Context7NotFoundError(Context7Error):
    """Library not found (404)."""
    pass


class Context7RateLimitError(Context7Error):
    """Rate limit exceeded (429)."""
    def __init__(self, message: str, retry_after_seconds: int | None = None):
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


def load_doc_sources() -> dict[str, dict[str, any]]:
    """
    Load documentation sources from .claude/doc-sources.toml.

    Returns:
        Dictionary mapping source names to their configuration.

    Raises:
        FileNotFoundError: If doc-sources.toml doesn't exist.
        Context7Error: If TOML parsing fails.
    """
    # Find doc-sources.toml (relative to this file)
    lib_dir = Path(__file__).parent
    skill_dir = lib_dir.parent  # .claude/skills/doc-query
    skills_dir = skill_dir.parent  # .claude/skills
    claude_dir = skills_dir.parent  # .claude
    config_path = claude_dir / "doc-sources.toml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            "Run 'add-doc' skill to configure documentation sources."
        )

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
            return config.get("sources", {})
    except Exception as e:
        raise Context7Error(f"Failed to parse {config_path}: {e}")


def resolve_source(name: str) -> tuple[str, int]:
    """
    Resolve a source name to its Context7 ID and default token limit.

    Args:
        name: Source name or alias (e.g., "python", "py", "claude-code")

    Returns:
        Tuple of (context7_id, default_tokens)

    Raises:
        Context7Error: If source not found.
    """
    sources = load_doc_sources()

    # Direct match
    if name in sources:
        source = sources[name]
        return source["context7_id"], source.get("default_tokens", 2500)

    # Check aliases
    for source_name, source_config in sources.items():
        aliases = source_config.get("aliases", [])
        if name in aliases:
            return source_config["context7_id"], source_config.get("default_tokens", 2500)

    # Not found
    available = list(sources.keys())
    raise Context7Error(
        f"Unknown documentation source: '{name}'\n"
        f"Available sources: {', '.join(available)}\n"
        f"Run '.claude/skills/doc-query/scripts/list-sources' to see all sources."
    )


def query_documentation(
    source: str,
    topic: str = "",
    tokens: int | None = None
) -> dict[str, str]:
    """
    Query Context7 documentation for a given source.

    Args:
        source: Source name from doc-sources.toml (e.g., "python", "claude-code")
        topic: Optional topic filter (e.g., "async context managers")
        tokens: Max tokens to return (uses source default if None)

    Returns:
        Dictionary with 'content' (markdown text), 'source', 'topic' keys.

    Raises:
        Context7AuthError: Invalid or missing API key
        Context7NotFoundError: Library not found
        Context7RateLimitError: Rate limit exceeded
        Context7Error: Other API errors

    Example:
        >>> docs = query_documentation("python", "async context managers", 2000)
        >>> print(docs['content'])
    """
    if not API_KEY:
        raise Context7AuthError(
            "CONTEXT7_API_KEY environment variable not set. "
            "See CONTRIBUTING.md for setup instructions."
        )

    # Resolve source name to Context7 ID
    context7_id, default_tokens = resolve_source(source)

    # Use default tokens if not specified
    if tokens is None:
        tokens = default_tokens

    # Build URL with query parameters
    url = f"{BASE_URL}/{context7_id}"

    params = {}
    if topic:
        params["topic"] = topic
    if tokens:
        params["tokens"] = str(tokens)

    if params:
        url += "?" + urlencode(params)

    # Build request with headers
    headers = {"Authorization": f"Bearer {API_KEY}"}
    request = Request(url, headers=headers)

    # Make request
    try:
        with urlopen(request, timeout=30) as response:
            data = response.read().decode('utf-8')
            # Context7 returns plain text markdown, not JSON
            return {"content": data, "source": source, "context7_id": context7_id, "topic": topic}

    except HTTPError as e:
        # Handle HTTP error responses
        error_body = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
        except json.JSONDecodeError:
            error_data = {"error": error_body}

        if e.code == 401:
            raise Context7AuthError("Invalid or missing API key")
        elif e.code == 404:
            raise Context7NotFoundError(f"Documentation not found: {context7_id}")
        elif e.code == 429:
            retry_after = error_data.get("retryAfterSeconds")
            raise Context7RateLimitError(
                f"Rate limit exceeded. Retry after {retry_after} seconds.",
                retry_after_seconds=retry_after
            )
        else:
            raise Context7Error(f"API error: {error_data.get('error', 'Unknown error')}")

    except URLError as e:
        raise Context7Error(f"Request failed: {e.reason}")
    except Exception as e:
        raise Context7Error(f"Unexpected error: {e}")
