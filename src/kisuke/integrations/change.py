"""Change detection.

Computes cheap, deterministic snapshots of the repository filesystem and
derives file-level changes (added / modified / removed) between two snapshots.
Changed Markdown files are best-effort mapped to their entity ID so callers can
react at the entity level. Detection never mutates the repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from kisuke.infrastructure.storage.serializer import markdown_to_entity

ChangeKind = Literal["added", "modified", "removed"]

GIT_DIR = ".git"


@dataclass
class FileChange:
    """A single detected filesystem change."""

    kind: ChangeKind
    path: str
    entity_id: str | None = None


@dataclass
class RepoSnapshot:
    """A point-in-time signature of repository files."""

    files: dict[str, tuple[int, int]] = field(default_factory=dict)


def _signature(path: Path) -> tuple[int, int]:
    stat = path.stat()
    return (stat.st_mtime_ns, stat.st_size)


def _is_ignored(rel: str, ignore: set[str]) -> bool:
    for entry in ignore:
        if rel == entry or rel.startswith(entry + "/"):
            return True
    return False


def snapshot(root: Path, ignore: set[str] | None = None) -> RepoSnapshot:
    """Capture (mtime, size) signatures for every file under ``root``.

    The ``.git`` directory is always excluded, and any additional relative paths
    provided in ``ignore`` (files or directories) are skipped. Derived artifacts
    such as the search index or sync cache must be excluded so change detection
    only reports canonical repository changes.
    """
    root = Path(root)
    ignore = set(ignore or set())
    files: dict[str, tuple[int, int]] = {}
    if root.is_dir():
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = str(path.relative_to(root))
            if rel.split("/", 1)[0] == GIT_DIR:
                continue
            if _is_ignored(rel, ignore):
                continue
            files[rel] = _signature(path)
    return RepoSnapshot(files=files)


def _entity_id_of(path: Path) -> str | None:
    try:
        entity = markdown_to_entity(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - best-effort mapping only
        return None
    return str(entity.id)


def detect_changes(before: RepoSnapshot, after: RepoSnapshot, root: Path) -> list[FileChange]:
    """Return the changes between two snapshots."""
    root = Path(root)
    changes: list[FileChange] = []
    before_files = before.files
    after_files = after.files

    for rel, sig in after_files.items():
        if rel not in before_files:
            entity_id = _entity_id_of(root / rel) if rel.endswith(".md") else None
            changes.append(FileChange("added", rel, entity_id))
        elif before_files[rel] != sig:
            entity_id = _entity_id_of(root / rel) if rel.endswith(".md") else None
            changes.append(FileChange("modified", rel, entity_id))

    for rel in before_files:
        if rel not in after_files:
            changes.append(FileChange("removed", rel, None))

    return changes


def summarize(changes: list[FileChange]) -> dict[str, int]:
    """Count changes by kind."""
    counts = {"added": 0, "modified": 0, "removed": 0}
    for change in changes:
        counts[change.kind] += 1
    return counts
