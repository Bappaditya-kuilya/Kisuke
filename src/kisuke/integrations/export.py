"""Export interface.

Exports repository entities to portable formats (a Markdown bundle directory or
a single JSON document). Export is strictly read-only: it never modifies the
repository or the search index.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kisuke.domain.entities import Entity
from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.storage.repository import FileRepository
from kisuke.infrastructure.storage.serializer import entity_to_markdown


@dataclass
class ExportResult:
    """Outcome of an export operation."""

    targets: list[str] = field(default_factory=list)
    count: int = 0


class Exporter:
    """Read-only export of repository entities."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.repo = FileRepository(self.root)

    def _all_entities(self) -> list[Entity]:
        entities: list[Entity] = []
        for entity_type in EntityType:
            entities.extend(self.repo.all(entity_type))
        return entities

    def export_bundle(self, target_dir: Path) -> ExportResult:
        """Write each entity as its canonical Markdown file into ``target_dir``."""
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        result = ExportResult()
        for entity in self._all_entities():
            sub = target_dir / entity.entity_type.value
            sub.mkdir(parents=True, exist_ok=True)
            path = sub / f"{entity.id}.md"
            path.write_text(entity_to_markdown(entity), encoding="utf-8")
            result.targets.append(str(path))
        result.count = len(result.targets)
        return result

    def export_json(self, target_path: Path) -> ExportResult:
        """Write all entities as a single JSON document."""
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload: list[dict[str, Any]] = [
            self._entity_to_dict(entity) for entity in self._all_entities()
        ]
        target_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        result = ExportResult(targets=[str(target_path)], count=len(payload))
        return result

    @staticmethod
    def _entity_to_dict(entity: Entity) -> dict[str, Any]:
        from kisuke.application.entities import entity_to_dict

        return entity_to_dict(entity)
