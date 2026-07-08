"""Tests for the Git integration adapter.

Git remains the system of record. Reads degrade gracefully when Git is absent
or the directory is not a repository; the explicit commit helper only writes
when called directly.
"""

from __future__ import annotations

from pathlib import Path

from kisuke.integrations import GitIntegration
from tests.integrations.conftest import make_populated


def test_not_a_repo(repo_root: Path) -> None:
    git = GitIntegration(repo_root)
    assert git.is_git_repo() is False
    assert git.is_available() is False


def test_is_repo_and_branch(git_repo: Path) -> None:
    git = GitIntegration(git_repo)
    assert git.is_git_repo() is True
    assert git.is_available() is True
    assert git.current_branch() is None  # no commits yet


def test_commit_and_recent_commits(git_repo: Path) -> None:
    (git_repo / "note.md").write_text("# note\n", encoding="utf-8")
    git = GitIntegration(git_repo)
    result = git.commit("add note")
    assert result is not None
    commits = git.recent_commits(5)
    assert len(commits) == 1
    assert commits[0]["message"] == "add note"
    assert git.current_branch() is not None


def test_status_clean_and_dirty(git_repo: Path) -> None:
    git = GitIntegration(git_repo)
    (git_repo / "x.md").write_text("# x\n", encoding="utf-8")
    git.commit("init")
    assert git.status()["clean"] is True
    (git_repo / "y.md").write_text("# y\n", encoding="utf-8")
    status = git.status()
    assert status["clean"] is False
    assert any("y.md" in change for change in status["changes"])


def test_snapshot_structure(git_repo: Path) -> None:
    git = GitIntegration(git_repo)
    (git_repo / "x.md").write_text("# x\n", encoding="utf-8")
    git.commit("init")
    snap = git.snapshot()
    assert snap["is_repo"] is True
    assert "commits" in snap and "status" in snap


def test_commit_via_registry(git_repo: Path, registry: object) -> None:
    from kisuke.plugins.registry import PluginRegistry

    make_populated(git_repo)
    integration = registry.get("git") if isinstance(registry, PluginRegistry) else None
    assert integration is not None
    message = integration.commit("add entities")  # type: ignore[union-attr]
    assert message is not None
