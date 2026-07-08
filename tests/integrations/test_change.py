"""Tests for change detection.

Covers snapshot capture, the added/modified/removed classification, the
``.git`` exclusion, derived-artifact ignoring, entity-ID mapping, and the
change summary helper.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from kisuke.integrations import detect_changes, snapshot, summarize
from tests.integrations.conftest import make_populated


def _init_git(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)


def test_snapshot_captures_files(repo_root: Path) -> None:
    (repo_root / "a.md").write_text("x", encoding="utf-8")
    snap = snapshot(repo_root)
    assert "a.md" in snap.files


def test_snapshot_excludes_git(repo_root: Path) -> None:
    _init_git(repo_root)
    (repo_root / "a.md").write_text("x", encoding="utf-8")
    snap = snapshot(repo_root)
    assert "a.md" in snap.files
    assert all(not key.startswith(".git") for key in snap.files)


def test_snapshot_ignores_derived_artifacts(repo_root: Path) -> None:
    (repo_root / "index.db").write_text("x", encoding="utf-8")
    (repo_root / "cache").mkdir()
    (repo_root / "cache" / "snap.json").write_text("{}", encoding="utf-8")
    snap = snapshot(repo_root, ignore={"index.db", "cache"})
    assert "index.db" not in snap.files
    assert "cache/snap.json" not in snap.files


def test_detect_added_modified_removed(repo_root: Path) -> None:
    (repo_root / "a.md").write_text("1", encoding="utf-8")
    before = snapshot(repo_root)
    (repo_root / "b.md").write_text("2", encoding="utf-8")
    (repo_root / "a.md").write_text("changed", encoding="utf-8")
    (repo_root / "c.md").write_text("3", encoding="utf-8")
    after = snapshot(repo_root)
    by_path = {c.path: c.kind for c in detect_changes(before, after, repo_root)}
    assert by_path.get("b.md") == "added"
    assert by_path.get("a.md") == "modified"
    (repo_root / "c.md").unlink()
    after2 = snapshot(repo_root)
    removed = [c for c in detect_changes(after, after2, repo_root) if c.kind == "removed"]
    assert any(c.path == "c.md" for c in removed)


def test_entity_id_mapping(repo_root: Path) -> None:
    ids = make_populated(repo_root)
    before = snapshot(repo_root)
    task_path = repo_root / "tasks" / f"{ids[2]}.md"
    text = task_path.read_text(encoding="utf-8")
    task_path.write_text(text + "\n<!-- edited -->\n", encoding="utf-8")
    after = snapshot(repo_root)
    suffix = f"{ids[2]}.md"
    mapped = [c for c in detect_changes(before, after, repo_root) if c.path.endswith(suffix)]
    assert mapped and mapped[0].entity_id == ids[2]


def test_summarize(repo_root: Path) -> None:
    (repo_root / "a.md").write_text("1", encoding="utf-8")
    before = snapshot(repo_root)
    (repo_root / "b.md").write_text("2", encoding="utf-8")
    after = snapshot(repo_root)
    counts = summarize(detect_changes(before, after, repo_root))
    assert counts == {"added": 1, "modified": 0, "removed": 0}
