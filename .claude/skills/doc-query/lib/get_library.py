"""
Get documentation for any library supported by Context7.

Generic wrapper for accessing documentation of libraries beyond Python and
Claude Code CLI. Useful for 3rd-party adapter development (AWS SDK, GCP SDK,
PostgreSQL drivers, etc.).
"""

from typing import Dict, Any, Optional
from . import _call_context7


def get_library_docs(
    library: str,
    topic: str = "",
    version: str = "",
    tokens: int = 5000
) -> Dict[str, Any]:
    """
    Get documentation for any library.

    Args:
        library: Library identifier (e.g., "vercel/next.js", "aws/aws-sdk")
        topic: Optional topic filter (e.g., "routing", "s3")
        version: Optional version (e.g., "v15.1.8", "3.x")
        tokens: Max tokens to return (default: 5000)

    Returns:
        Documentation results as dictionary

    Example:
        >>> # Agent queries AWS SDK documentation for adapter development
        >>> results = get_library_docs(
        ...     library="aws/aws-sdk-python",
        ...     topic="s3 client",
        ...     tokens=4000
        ... )
        >>>
        >>> # Filter for async examples
        >>> async_examples = [
        ...     snippet for snippet in results.get("snippets", [])
        ...     if "async" in snippet.get("content", "")
        ... ]
        >>>
        >>> return async_examples

    Raises:
        Context7AuthError: Invalid or missing API key
        Context7NotFoundError: Library not found
        Context7RateLimitError: Rate limit exceeded
    """
    return _call_context7(library, version=version, topic=topic, tokens=tokens)
