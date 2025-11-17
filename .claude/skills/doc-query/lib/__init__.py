"""
Documentation query library for Context7 API access.

This package provides token-efficient documentation queries for configured
tool and technology sources.
"""

from .context7_client import (
    query_documentation,
    load_doc_sources,
    resolve_source,
    Context7Error,
    Context7AuthError,
    Context7NotFoundError,
    Context7RateLimitError,
)

__all__ = [
    "query_documentation",
    "load_doc_sources",
    "resolve_source",
    "Context7Error",
    "Context7AuthError",
    "Context7NotFoundError",
    "Context7RateLimitError",
]
