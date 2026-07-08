"""SQLite-backed inverted index builder.

Stores entities and a token inverted index in SQLite (a local, dependency-free
index). The index is always rebuildable from the Markdown source; incremental
updates use a content hash to skip unchanged entities.
"""

from __future__ import annotations

import hashlib
from typing import Any

from kisuke.domain.entities import Entity
from kisuke.infrastructure.search.ranking import tokenize

SCHEMA = """
CREATE TABLE IF NOT EXISTS entities (
    id            TEXT PRIMARY KEY,
    type          TEXT NOT NULL,
    title         TEXT NOT NULL,
    owner         TEXT NOT NULL,
    status        TEXT NOT NULL,
    tags          TEXT NOT NULL,
    body          TEXT NOT NULL,
    content_hash  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tokens (
    token      TEXT NOT NULL,
    entity_id  TEXT NOT NULL,
    field      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_token ON tokens(token);
CREATE INDEX IF NOT EXISTS idx_type ON entities(type);
CREATE INDEX IF NOT EXISTS idx_owner ON entities(owner);
CREATE INDEX IF NOT EXISTS idx_status ON entities(status);
"""


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _owner_str(entity: Entity) -> str:
    if entity.owner.sentinel is not None:
        return entity.owner.sentinel
    assert entity.owner.entity_id is not None
    return str(entity.owner.entity_id)


class IndexBuilder:
    """Builds and maintains the SQLite search index."""

    def __init__(self, conn: Any) -> None:
        self.conn = conn
        self.upsert_count = 0

    def initialize(self) -> None:
        self.conn.executescript(SCHEMA)

    def reset(self) -> None:
        self.conn.execute("DELETE FROM entities")
        self.conn.execute("DELETE FROM tokens")
        self.upsert_count = 0

    def get_hash(self, entity_id: str) -> str | None:
        row = self.conn.execute(
            "SELECT content_hash FROM entities WHERE id=?", (entity_id,)
        ).fetchone()
        return row[0] if row else None

    def all_ids(self) -> set[str]:
        return {row[0] for row in self.conn.execute("SELECT id FROM entities")}

    def remove(self, entity_id: str) -> None:
        self.conn.execute("DELETE FROM tokens WHERE entity_id=?", (entity_id,))
        self.conn.execute("DELETE FROM entities WHERE id=?", (entity_id,))

    def upsert(self, entity: Entity, body: str, content_hash: str) -> None:
        entity_id = str(entity.id)
        self.conn.execute("DELETE FROM tokens WHERE entity_id=?", (entity_id,))
        self.conn.execute("DELETE FROM entities WHERE id=?", (entity_id,))
        self.conn.execute(
            "INSERT INTO entities (id, type, title, owner, status, tags, body, content_hash) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entity_id,
                entity.entity_type.value,
                entity.title,
                _owner_str(entity),
                str(entity.status),
                " ".join(entity.tags),
                body,
                content_hash,
            ),
        )
        for token in tokenize(entity.title):
            self.conn.execute(
                "INSERT INTO tokens (token, entity_id, field) VALUES (?, ?, 'title')",
                (token, entity_id),
            )
        for token in tokenize(" ".join(entity.tags)):
            self.conn.execute(
                "INSERT INTO tokens (token, entity_id, field) VALUES (?, ?, 'tag')",
                (token, entity_id),
            )
        for token in tokenize(body):
            self.conn.execute(
                "INSERT INTO tokens (token, entity_id, field) VALUES (?, ?, 'body')",
                (token, entity_id),
            )
        self.upsert_count += 1
