"""Deterministic ordering for resume results.

Entities are ordered by a coarse lifecycle rank (active work first) and then by
ID, guaranteeing stable, reproducible output across runs.
"""

from __future__ import annotations

from collections.abc import Sequence

from kisuke.domain.entities import Entity


def _status_rank(value: str) -> int:
    v = value.lower().replace(" ", "")
    if "active" in v or "inprogress" in v:
        return 0
    if any(k in v for k in ("todo", "planning", "proposed", "scheduled", "paused")):
        return 1
    if "blocked" in v:
        return 2
    if any(k in v for k in ("done", "completed")):
        return 3
    if any(k in v for k in ("archived", "unavailable", "superseded")):
        return 4
    return 5


def order_entities(entities: Sequence[Entity]) -> list[Entity]:
    """Order entities by (status rank, id) for deterministic output."""
    return sorted(entities, key=lambda e: (_status_rank(str(e.status)), str(e.id)))
