"""Search result model.

A lightweight, deterministic representation of a single search hit.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    """One hit returned by the search engine."""

    entity_id: str
    entity_type: str
    title: str
    owner: str
    status: str
    score: float = 0.0
