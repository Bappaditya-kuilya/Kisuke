"""Search application service.

Wraps the offline :class:`SearchEngine`, keeping the index in sync with the
repository before every query so results are always current.
"""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.search.api import SearchEngine
from kisuke.infrastructure.search.model import SearchResult


class SearchService:
    """Offline search over the Markdown repository."""

    def __init__(self, root: Path, db_path: Path) -> None:
        self.root = Path(root)
        self.db_path = Path(db_path)

    def _engine(self) -> SearchEngine:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return SearchEngine(self.db_path)

    def search(self, query: str, entity_type: str | None = None) -> list[SearchResult]:
        with self._engine() as engine:
            engine.update(self.root)
            return engine.search(query, type=entity_type)

    def get_by_id(self, entity_id: str) -> SearchResult | None:
        with self._engine() as engine:
            engine.update(self.root)
            return engine.get_by_id(entity_id)
