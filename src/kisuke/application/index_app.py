"""Index application service.

Builds, updates, and cleans the offline search index. These are thin wrappers
over the :class:`SearchEngine` public API.
"""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.search.api import SearchEngine


class IndexService:
    """Manage the SQLite search index lifecycle."""

    def __init__(self, root: Path, db_path: Path) -> None:
        self.root = Path(root)
        self.db_path = Path(db_path)

    def build(self) -> int:
        with self._engine() as engine:
            engine.rebuild(self.root)
            return engine.builder.upsert_count

    def update(self) -> int:
        with self._engine() as engine:
            engine.update(self.root)
            return engine.builder.upsert_count

    def clean(self) -> bool:
        if self.db_path.exists():
            self.db_path.unlink()
            return True
        return False

    def _engine(self) -> SearchEngine:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return SearchEngine(self.db_path)
