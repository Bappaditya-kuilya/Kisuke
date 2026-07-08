"""Markdown import adapter.

Imports external Markdown files into the Kisuke repository as canonical
entities. Import is strictly additive and safe: existing entity IDs are skipped
unless ``overwrite`` is explicitly requested, so canonical data is never mutated
unexpectedly. All writes go through the Storage repository, preserving
validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from kisuke.domain.exceptions import ValidationError
from kisuke.infrastructure.storage.repository import FileRepository
from kisuke.infrastructure.storage.serializer import markdown_to_entity


@dataclass
class ImportResult:
    """Outcome of an import operation."""

    imported: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class MarkdownImporter:
    """Import Markdown files into the repository as entities."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.repo = FileRepository(self.root)

    def import_file(self, path: Path, overwrite: bool = False) -> ImportResult:
        path = Path(path)
        result = ImportResult()
        try:
            text = path.read_text(encoding="utf-8")
            entity = markdown_to_entity(text)
        except Exception as exc:  # noqa: BLE001 - report and continue
            result.errors.append(f"{path}: {exc}")
            return result
        if self.repo.exists(entity.entity_type, entity.id) and not overwrite:
            result.skipped.append(str(entity.id))
            return result
        try:
            self.repo.save(entity)
        except ValidationError as exc:
            result.errors.append(f"{path}: {'; '.join(exc.problems)}")
            return result
        result.imported.append(str(entity.id))
        return result

    def import_directory(
        self, path: Path, recursive: bool = False, overwrite: bool = False
    ) -> ImportResult:
        path = Path(path)
        result = ImportResult()
        pattern = "**/*.md" if recursive else "*.md"
        for file in sorted(path.glob(pattern)):
            if file.is_file():
                part = self.import_file(file, overwrite=overwrite)
                result.imported.extend(part.imported)
                result.skipped.extend(part.skipped)
                result.errors.extend(part.errors)
        return result
