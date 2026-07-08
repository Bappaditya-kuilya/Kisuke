"""Repository scanner.

Discovers entity Markdown files under the canonical type-specific folders
defined by the Storage layer. Read-only: never modifies the repository.
"""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.storage.repository import FOLDER_NAMES


class RepositoryScanner:
    """Walks the canonical entity folders and discovers Markdown files."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def discover(self) -> list[Path]:
        """Return every ``*.md`` entity file, sorted by path for determinism."""
        found: list[Path] = []
        for folder in FOLDER_NAMES.values():
            directory = self.root / folder
            if directory.is_dir():
                found.extend(sorted(directory.glob("*.md")))
        return sorted(found)
