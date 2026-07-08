"""File-backed Markdown repository.

Stores one entity per Markdown file under a type-specific folder. Writes are
atomic (temp file + os.replace). Loaded entities are validated against the
Domain Model via validate_entity / validate_entities.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from kisuke.domain.entities import Entity
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import EntityType
from kisuke.domain.validation import validate_entities, validate_entity

from .interfaces import EntityRepository, RepositoryError
from .serializer import entity_to_markdown, markdown_to_entity

FOLDER_NAMES: dict[EntityType, str] = {
    EntityType.MISSION: "missions",
    EntityType.PROJECT: "projects",
    EntityType.TASK: "tasks",
    EntityType.KNOWLEDGE: "knowledge",
    EntityType.COOKBOOK: "cookbook",
    EntityType.DECISION: "decisions",
    EntityType.MEETING: "meetings",
    EntityType.PERSON: "people",
    EntityType.RESOURCE: "resources",
    EntityType.REVIEW: "reviews",
    EntityType.ATTACHMENT: "attachments",
}


class FileRepository(EntityRepository):
    """Stores entities as Markdown files rooted at a directory."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def _folder(self, entity_type: EntityType) -> Path:
        return self.root / FOLDER_NAMES[entity_type]

    def _path(self, entity_type: EntityType, entity_id: EntityId) -> Path:
        return self._folder(entity_type) / f"{entity_id}.md"

    def save(self, entity: Entity) -> None:
        validate_entity(entity)
        folder = self._folder(entity.entity_type)
        folder.mkdir(parents=True, exist_ok=True)
        path = self._path(entity.entity_type, entity.id)
        self._atomic_write(path, entity_to_markdown(entity))

    def _atomic_write(self, path: Path, text: str) -> None:
        fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
            os.replace(tmp_name, path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def load(self, entity_type: EntityType, entity_id: EntityId) -> Entity:
        path = self._path(entity_type, entity_id)
        if not path.exists():
            raise RepositoryError(f"No {entity_type} with id {entity_id}")
        return markdown_to_entity(path.read_text(encoding="utf-8"), entity_type)

    def delete(self, entity_type: EntityType, entity_id: EntityId) -> None:
        path = self._path(entity_type, entity_id)
        if path.exists():
            path.unlink()

    def exists(self, entity_type: EntityType, entity_id: EntityId) -> bool:
        return self._path(entity_type, entity_id).exists()

    def all(self, entity_type: EntityType) -> list[Entity]:
        folder = self._folder(entity_type)
        if not folder.exists():
            return []
        entities: list[Entity] = []
        for path in sorted(folder.glob("*.md")):
            entities.append(markdown_to_entity(path.read_text(encoding="utf-8"), entity_type))
        return entities

    def load_by_id(self, entity_id: EntityId) -> Entity:
        for entity_type in FOLDER_NAMES:
            if self.exists(entity_type, entity_id):
                return self.load(entity_type, entity_id)
        raise RepositoryError(f"No entity with id {entity_id}")

    def validate_repository(self) -> None:
        """Validate every stored entity against the Domain Model."""
        entities: list[Entity] = []
        for entity_type in FOLDER_NAMES:
            entities.extend(self.all(entity_type))
        validate_entities(entities)
