"""Synchronization service.

Keeps derived state (the search index) in sync with the canonical Markdown
repository using incremental change detection. On each run it compares the
current filesystem snapshot against the previous one, applies an incremental
index update, and persists the new snapshot. Optionally, when a Git integration
is provided, changed entity files can be committed (explicit, user-approved).

Sync never modifies canonical Markdown except through the explicit, optional Git
commit path; the incremental index update is rebuildable and non-destructive.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kisuke.application.index_app import IndexService
from kisuke.integrations.change import (
    FileChange,
    RepoSnapshot,
    detect_changes,
    snapshot,
    summarize,
)


@dataclass
class SyncResult:
    """Outcome of an incremental synchronization run."""

    changes: list[FileChange] = field(default_factory=list)
    indexed: int = 0
    baseline: bool = False
    committed: str | None = None

    def summary(self) -> dict[str, int]:
        return summarize(self.changes)


class SyncService:
    """Incrementally synchronize the repository with its derived index."""

    def __init__(
        self,
        root: Path,
        db_path: Path,
        cache_dir: Path | None = None,
        git: Any | None = None,
    ) -> None:
        self.root = Path(root)
        self.db_path = Path(db_path)
        self.cache_dir = Path(cache_dir) if cache_dir is not None else None
        self.git = git

    def _snapshot_path(self) -> Path:
        assert self.cache_dir is not None
        return self.cache_dir / "sync_snapshot.json"

    def _ignored(self) -> set[str]:
        ignore: set[str] = set()
        if self.cache_dir is not None and self.cache_dir.is_relative_to(self.root):
            ignore.add(str(self.cache_dir.relative_to(self.root)))
        if self.db_path.is_relative_to(self.root):
            ignore.add(str(self.db_path.relative_to(self.root)))
        return ignore

    def _load_previous(self) -> RepoSnapshot | None:
        if self.cache_dir is None or not self._snapshot_path().exists():
            return None
        try:
            raw = json.loads(self._snapshot_path().read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return None
        if not isinstance(raw, dict):
            return None
        files: dict[str, tuple[int, int]] = {}
        for key, value in raw.items():
            if isinstance(value, (list, tuple)) and len(value) == 2:
                files[key] = (int(value[0]), int(value[1]))
        return RepoSnapshot(files=files)

    def _save_snapshot(self, snap: RepoSnapshot) -> None:
        if self.cache_dir is None:
            return
        self._snapshot_path().parent.mkdir(parents=True, exist_ok=True)
        self._snapshot_path().write_text(json.dumps(snap.files), encoding="utf-8")

    def sync_incremental(self) -> SyncResult:
        """Detect changes and apply an incremental index update."""
        previous = self._load_previous()
        current = snapshot(self.root, self._ignored())
        changes = detect_changes(previous, current, self.root) if previous is not None else []
        indexed = IndexService(self.root, self.db_path).update()
        self._save_snapshot(current)
        return SyncResult(changes=changes, indexed=indexed, baseline=previous is None)

    def commit_changes(self, message: str) -> str | None:
        """Commit changed entity files via the Git integration, if available."""
        if self.git is None or not self.git.is_available():
            return None
        changed = [
            str(self.root / change.path)
            for change in self._pending_changes()
            if change.kind != "removed"
        ]
        if not changed:
            return None
        committed: str | None = self.git.commit(message, changed)
        return committed

    def _pending_changes(self) -> list[FileChange]:
        previous = self._load_previous()
        if previous is None:
            return []
        return detect_changes(previous, snapshot(self.root), self.root)
