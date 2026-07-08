"""Deterministic ranking for search results.

Tokens are simple word fragments; ranking is a transparent, reproducible
function of token weights and alphabetical tie-breakers. No external scoring
engine is used.
"""

from __future__ import annotations

import re

from .model import SearchResult

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")

TITLE_WEIGHT = 5.0
TAG_WEIGHT = 3.0
BODY_WEIGHT = 1.0


def tokenize(text: str) -> list[str]:
    """Lowercase, extract word tokens."""
    if not text:
        return []
    return TOKEN_PATTERN.findall(text.lower())


def field_weight(field: str) -> float:
    """Weight of a matched token by the field it was indexed from."""
    if field == "title":
        return TITLE_WEIGHT
    if field == "tag":
        return TAG_WEIGHT
    return BODY_WEIGHT


def sort_results(results: list[SearchResult]) -> list[SearchResult]:
    """Deterministic ordering: highest score, then title, then id."""
    return sorted(results, key=lambda r: (-r.score, r.title.lower(), r.entity_id))
