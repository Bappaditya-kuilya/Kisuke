"""Search engine API.

Wraps the SQLite index builder with a repository-aware rebuild/update and a
deterministic query API: free-text search with type/owner/status filtering,
exact ID lookup, and rebuildable indexing.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from kisuke.domain.entities import Entity
from kisuke.infrastructure.search.index import IndexBuilder, hash_content
from kisuke.infrastructure.search.model import SearchResult
from kisuke.infrastructure.search.ranking import field_weight, sort_results, tokenize
from kisuke.infrastructure.storage.frontmatter import split_markdown
from kisuke.infrastructure.validation.parser import IncrementalParser
from kisuke.infrastructure.validation.scanner import RepositoryScanner


class SearchEngine:
    """Local, offline search over the Markdown repository."""

    def __init__(self, db_path: str | Path) -> None:
        self.conn: Any = sqlite3.connect(str(db_path))
        self.builder = IndexBuilder(self.conn)
        self.builder.initialize()
        self._parser = IncrementalParser()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> SearchEngine:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------
    def rebuild(self, root: str | Path) -> None:
        """Drop and fully rebuild the index from the repository."""
        self.builder.reset()
        for entity, body, content_hash in self._iter_entities(root):
            self.builder.upsert(entity, body, content_hash)
        self.conn.commit()

    def update(self, root: str | Path) -> None:
        """Incrementally update the index; unchanged entities are skipped."""
        current_ids: set[str] = set()
        for entity, body, content_hash in self._iter_entities(root):
            entity_id = str(entity.id)
            current_ids.add(entity_id)
            if self.builder.get_hash(entity_id) == content_hash:
                continue
            self.builder.upsert(entity, body, content_hash)
        for stale in self.builder.all_ids() - current_ids:
            self.builder.remove(stale)
        self.conn.commit()

    def _iter_entities(self, root: str | Path) -> Iterator[tuple[Entity, str, str]]:
        scanner = RepositoryScanner(Path(root))
        for path in scanner.discover():
            result = self._parser.parse_file(path)
            if result.entity is None:
                continue
            text = path.read_text(encoding="utf-8")
            _, body = split_markdown(text)
            yield result.entity, body, hash_content(text)

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------
    def search(
        self,
        query: str,
        type: str | None = None,
        owner: str | None = None,
        status: str | None = None,
    ) -> list[SearchResult]:
        tokens = tokenize(query)
        if not tokens:
            return []

        scores: dict[str, float] = {}
        for token in tokens:
            for entity_id, field in self.conn.execute(
                "SELECT entity_id, field FROM tokens WHERE token=?", (token,)
            ):
                scores[entity_id] = scores.get(entity_id, 0.0) + field_weight(field)

        results: list[SearchResult] = []
        for entity_id in scores:
            row = self.conn.execute(
                "SELECT id, type, title, owner, status FROM entities WHERE id=?",
                (entity_id,),
            ).fetchone()
            if row is None:
                continue
            hit_id, hit_type, title, hit_owner, hit_status = row
            if type is not None and type != hit_type:
                continue
            if owner is not None and owner != hit_owner:
                continue
            if status is not None and status != hit_status:
                continue
            results.append(
                SearchResult(hit_id, hit_type, title, hit_owner, hit_status, scores[entity_id])
            )
        return sort_results(results)

    def get_by_id(self, entity_id: str) -> SearchResult | None:
        row = self.conn.execute(
            "SELECT id, type, title, owner, status FROM entities WHERE id=?",
            (entity_id,),
        ).fetchone()
        if row is None:
            return None
        hit_id, hit_type, title, hit_owner, hit_status = row
        return SearchResult(hit_id, hit_type, title, hit_owner, hit_status, 0.0)
