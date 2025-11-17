"""
Search Claude Code CLI documentation.

Provides direct API access to Claude Code CLI documentation for code execution.
Essential for understanding Skills, MCP integration, slash commands, and other
Claude Code CLI features that may not be in base LLM training data.
"""

from typing import Dict, Any
from . import _call_context7


def search_claude_code_docs(topic: str, tokens: int = 5000) -> Dict[str, Any]:
    """
    Search Claude Code CLI documentation.

    Args:
        topic: What to search for (e.g., "skills", "mcp", "slash commands", "hooks")
        tokens: Max tokens to return (default: 5000)

    Returns:
        Documentation results as dictionary containing:
        - content: Plain text markdown documentation
        - library: Library identifier
        - topic: Search topic

    Example:
        >>> # Agent writes code to find MCP server documentation
        >>> results = search_claude_code_docs("mcp server", tokens=3000)
        >>>
        >>> # Process markdown locally (huge token savings!)
        >>> content = results.get("content", "")
        >>> lines = content.split('\n')
        >>> install_steps = [l for l in lines if "install" in l.lower()]
        >>>
        >>> return install_steps

    Raises:
        Context7AuthError: Invalid or missing API key
        Context7NotFoundError: Claude Code docs not found
        Context7RateLimitError: Rate limit exceeded
    """
    return _call_context7("websites/code_claude", topic=topic, tokens=tokens)
