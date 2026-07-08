"""Infrastructure search package.

Pure Infrastructure layer: a local, offline, dependency-free full-text search
index over the Markdown repository. The index is rebuildable from source and
supports filtering by type, owner, and status.
"""

from __future__ import annotations

from .api import SearchEngine
from .index import IndexBuilder, hash_content
from .model import SearchResult
from .ranking import field_weight, sort_results, tokenize

__all__ = [
    "SearchEngine",
    "IndexBuilder",
    "hash_content",
    "SearchResult",
    "field_weight",
    "sort_results",
    "tokenize",
]
