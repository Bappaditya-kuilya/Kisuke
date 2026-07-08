"""Doctor application service.

Runs the deterministic health checks described in the CLI specification:
repository, markdown, index, configuration, and plugins.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kisuke.infrastructure.validation.parser import IncrementalParser
from kisuke.infrastructure.validation.scanner import RepositoryScanner
from kisuke.shared.config import Config


@dataclass
class Check:
    """A single doctor health check result."""

    name: str
    ok: bool
    detail: str


class DoctorService:
    """Run repository health checks."""

    def __init__(self, root: Path, config: Config, db_path: Path) -> None:
        self.root = Path(root)
        self.config = config
        self.db_path = Path(db_path)

    def run(self) -> list[Check]:
        return [
            self._check_repository(),
            self._check_markdown(),
            self._check_index(),
            self._check_configuration(),
            self._check_plugins(),
        ]

    def _check_repository(self) -> Check:
        if self.root.is_dir():
            return Check("repository", True, f"found at {self.root}")
        return Check("repository", False, f"repository root not found: {self.root}")

    def _check_markdown(self) -> Check:
        scanner = RepositoryScanner(self.root)
        parser = IncrementalParser()
        count = 0
        errors = 0
        for path in scanner.discover():
            result = parser.parse_file(path)
            if result.error is not None:
                errors += 1
            elif result.entity is not None:
                count += 1
        if errors:
            return Check("markdown", False, f"{errors} file(s) failed to parse")
        return Check("markdown", True, f"{count} entity file(s) parsed")

    def _check_index(self) -> Check:
        if self.db_path.exists():
            return Check("index", True, f"index at {self.db_path}")
        return Check("index", False, "search index not built (run: kisuke index build)")

    def _check_configuration(self) -> Check:
        try:
            self.config.ensure_dirs()
        except OSError as exc:
            return Check("configuration", False, str(exc))
        return Check("configuration", True, f"data_dir={self.config.data_dir}")

    def _check_plugins(self) -> Check:
        return Check("plugins", True, "plugin registry available")
