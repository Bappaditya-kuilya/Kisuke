"""Tests for the filesystem watcher.

The watcher is poll-based and never mutates the repository. It reports
incremental added/modified/removed changes and supports an optional change
callback plus background threading.
"""

from __future__ import annotations

import time
from pathlib import Path

from kisuke.integrations import FileSystemWatcher


def test_first_poll_is_baseline(repo_root: Path) -> None:
    watcher = FileSystemWatcher(repo_root)
    assert watcher.poll_once() == []


def test_detects_added(repo_root: Path) -> None:
    watcher = FileSystemWatcher(repo_root)
    watcher.poll_once()
    (repo_root / "a.md").write_text("# a\n", encoding="utf-8")
    changes = watcher.poll_once()
    assert len(changes) == 1
    assert changes[0].kind == "added"
    assert changes[0].path == "a.md"


def test_detects_modified_and_removed(repo_root: Path) -> None:
    (repo_root / "b.md").write_text("# b\n", encoding="utf-8")
    watcher = FileSystemWatcher(repo_root)
    watcher.poll_once()
    (repo_root / "b.md").write_text("# b changed\n", encoding="utf-8")
    (repo_root / "c.md").write_text("# c\n", encoding="utf-8")
    kinds = {c.path: c.kind for c in watcher.poll_once()}
    assert kinds.get("b.md") == "modified"
    assert kinds.get("c.md") == "added"
    (repo_root / "c.md").unlink()
    removed = watcher.poll_once()
    assert removed[0].kind == "removed"
    assert removed[0].path == "c.md"


def test_callback_invoked(repo_root: Path) -> None:
    seen: list = []
    watcher = FileSystemWatcher(repo_root, on_change=lambda ch, _snap: seen.extend(ch))
    watcher.poll_once()
    (repo_root / "d.md").write_text("# d\n", encoding="utf-8")
    watcher.poll_once()
    assert any(c.kind == "added" for c in seen)


def test_ignore_excludes_derived(repo_root: Path) -> None:
    (repo_root / "cache").mkdir()
    watcher = FileSystemWatcher(repo_root, ignore={"cache"})
    watcher.poll_once()
    (repo_root / "cache" / "x.json").write_text("{}", encoding="utf-8")
    assert watcher.poll_once() == []


def test_start_stop_background(repo_root: Path) -> None:
    seen: list = []
    watcher = FileSystemWatcher(
        repo_root,
        on_change=lambda ch, _snap: seen.extend(ch),
        interval=0.05,
    )
    watcher.poll_once()
    watcher.start()
    (repo_root / "e.md").write_text("# e\n", encoding="utf-8")
    time.sleep(0.3)
    watcher.stop()
    assert any(c.kind == "added" for c in seen)
