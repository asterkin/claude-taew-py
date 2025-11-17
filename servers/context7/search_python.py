"""
Search Python 3.14+ documentation.

Provides direct API access to Python documentation for code execution.
Agent can write Python code to query and process documentation locally,
achieving significant token savings over traditional MCP approach.
"""

from typing import Dict, Any
from . import _call_context7


def search_python_docs(topic: str, tokens: int = 5000) -> Dict[str, Any]:
    """
    Search Python 3.14+ documentation.

    Args:
        topic: What to search for (e.g., "async generators", "type parameters", "match statement")
        tokens: Max tokens to return (default: 5000)

    Returns:
        Documentation results as dictionary containing:
        - snippets: List of relevant code examples and documentation
        - metadata: Source information and relevance scores

    Example:
        >>> # Agent writes code to query and filter locally
        >>> results = search_python_docs("async context managers", tokens=2000)
        >>>
        >>> # Filter results locally (massive token savings!)
        >>> relevant = [
        ...     snippet for snippet in results.get("snippets", [])
        ...     if "async with" in snippet.get("content", "")
        ... ]
        >>>
        >>> # Return only what's needed
        >>> return relevant[:3]

    Raises:
        Context7AuthError: Invalid or missing API key
        Context7NotFoundError: Python docs not found
        Context7RateLimitError: Rate limit exceeded
    """
    return _call_context7("python", version="3.14", topic=topic, tokens=tokens)
