"""
Context7 API client for code execution.

This module provides direct API access to Context7 documentation service,
enabling token-efficient documentation queries through code execution rather
than MCP server communication.

Uses Python 3.12+ stdlib only (urllib) - no external dependencies required.

See ADR-0003 for architectural rationale.
"""

import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from typing import Optional, Dict, Any


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
    def __init__(self, message: str, retry_after_seconds: Optional[int] = None):
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


def _call_context7(
    library: str,
    version: str = "",
    topic: str = "",
    tokens: int = 5000
) -> Dict[str, Any]:
    """
    Call Context7 API and return results.

    Args:
        library: Library name (e.g., "python", "claude-code")
        version: Optional version string (e.g., "3.14", "v15.1.8")
        topic: Optional topic filter (e.g., "routing", "async")
        tokens: Max tokens to return (default: 5000)

    Returns:
        Documentation results as dictionary

    Raises:
        Context7AuthError: Invalid or missing API key
        Context7NotFoundError: Library not found
        Context7RateLimitError: Rate limit exceeded
        Context7Error: Other API errors

    Example:
        >>> docs = _call_context7("python", version="3.14", topic="async", tokens=2000)
    """
    if not API_KEY:
        raise Context7AuthError(
            "CONTEXT7_API_KEY environment variable not set. "
            "See CONTRIBUTING.md for setup instructions."
        )

    # Build URL with query parameters
    url = f"{BASE_URL}/{library}"
    if version:
        url += f"/{version}"

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
            return {"content": data, "library": library, "version": version, "topic": topic}

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
            raise Context7NotFoundError(f"Library not found: {library}")
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
