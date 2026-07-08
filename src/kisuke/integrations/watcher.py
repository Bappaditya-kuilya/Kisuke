"""Filesystem watcher.

Polls the repository directory and emits incremental change events. Polling is
used instead of an external watchdog dependency so the integration stays
dependency-free and cross-platform. On each poll it computes a snapshot,
detects changes against the previous snapshot, and invokes an optional callback.
The watcher never modifies the repository; callers decide what to do (e.g.
trigger an incremental index update via the sync service).
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from pathlib import Path

from kisuke.integrations.change import (
    FileChange,
    RepoSnapshot,
    detect_changes,
    snapshot,
)

ChangeCallback = Callable[[list[FileChange], RepoSnapshot], None]


class FileSystemWatcher:
    """Poll-based watcher that reports incremental filesystem changes."""

    def __init__(
        self,
        root: Path,
        on_change: ChangeCallback | None = None,
        interval: float = 1.0,
        ignore: set[str] | None = None,
    ) -> None:
        self.root = Path(root)
        self.on_change = on_change
        self.interval = interval
        self.ignore = set(ignore or set())
        self._previous: RepoSnapshot | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def poll_once(self) -> list[FileChange]:
        """Take a snapshot, detect changes vs the previous one, return them."""
        current = snapshot(self.root, self.ignore)
        if self._previous is None:
            self._previous = current
            return []
        changes = detect_changes(self._previous, current, self.root)
        self._previous = current
        if changes and self.on_change is not None:
            self.on_change(changes, current)
        return changes

    def watch(self) -> None:
        """Block and poll until :meth:`stop` is called."""
        while not self._stop.is_set():
            self.poll_once()
            self._stop.wait(self.interval)

    def start(self) -> None:
        """Start watching in a background thread."""
        if self._thread is not None:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self.watch, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop a background watch thread, if running."""
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=self.interval + 1.0)
            self._thread = None
