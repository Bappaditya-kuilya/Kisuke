"""Tests for the synchronization service.

Sync keeps the derived search index in step with the canonical Markdown
repository via incremental change detection. It must ignore derived artifacts
(the index database and the sync cache) and only report canonical changes.
"""

from __future__ import annotations

from pathlib import Path

from kisuke.application.entities import build_entity
from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.storage.repository import FileRepository
from kisuke.integrations import GitIntegration, SyncService
from tests.integrations.conftest import make_populated


def test_baseline_builds_index(repo_root: Path, data_dir: Path) -> None:
    make_populated(repo_root)
    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    service = SyncService(repo_root, db, cache)
    result = service.sync_incremental()
    assert result.baseline is True
    assert result.indexed >= 3
    assert result.changes == []


def test_incremental_detects_modification(repo_root: Path, data_dir: Path) -> None:
    ids = make_populated(repo_root)
    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    service = SyncService(repo_root, db, cache)
    service.sync_incremental()

    task = repo_root / "tasks" / f"{ids[2]}.md"
    task.write_text(task.read_text(encoding="utf-8") + "\n<!-- edited -->\n", encoding="utf-8")

    result = service.sync_incremental()
    assert result.baseline is False
    assert any(c.kind == "modified" for c in result.changes)
    assert all(not c.path.endswith("index.db") for c in result.changes)


def test_sync_no_derived_noise(repo_root: Path, data_dir: Path) -> None:
    make_populated(repo_root)
    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    service = SyncService(repo_root, db, cache)
    service.sync_incremental()
    result = service.sync_incremental()
    assert result.changes == []


def test_sync_adds_new_entity(repo_root: Path, data_dir: Path) -> None:
    ids = make_populated(repo_root)
    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    service = SyncService(repo_root, db, cache)
    service.sync_incremental()

    repo = FileRepository(repo_root)
    new_task = build_entity(EntityType.TASK, {"title": "Fresh", "project": ids[1]})
    repo.save(new_task)

    result = service.sync_incremental()
    assert any(c.kind == "added" and c.entity_id == str(new_task.id) for c in result.changes)


def test_commit_changes_with_git(git_repo: Path, data_dir: Path) -> None:
    ids = make_populated(git_repo)
    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    git = GitIntegration(git_repo)
    git.commit("init entities")

    service = SyncService(git_repo, db, cache, git=git)
    service.sync_incremental()

    task = git_repo / "tasks" / f"{ids[2]}.md"
    task.write_text(task.read_text(encoding="utf-8") + "\n<!-- edited -->\n", encoding="utf-8")

    committed = service.commit_changes("update task")
    assert committed is not None


def test_commit_without_git_is_noop(repo_root: Path, data_dir: Path) -> None:
    make_populated(repo_root)
    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    service = SyncService(repo_root, db, cache)
    service.sync_incremental()
    assert service.commit_changes("nothing") is None
