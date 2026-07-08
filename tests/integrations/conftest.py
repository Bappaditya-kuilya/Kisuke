"""Shared fixtures for integration tests."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from kisuke.application.entities import build_entity
from kisuke.domain.entities import Mission, Project, Task
from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.storage.repository import FileRepository
from kisuke.integrations import build_registry


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir(parents=True, exist_ok=True)
    return root


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def registry(repo_root: Path, data_dir: Path) -> object:
    return build_registry(repo_root, data_dir / "integrations.json")


@pytest.fixture
def git_repo(repo_root: Path) -> Path:
    if shutil.which("git") is None:
        pytest.skip("git is not available")
    repo_root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@kisuke.local"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Kisuke Test"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    return repo_root


def make_populated(repo_root: Path) -> tuple[str, str, str]:
    """Create a mission, project, and task; return their IDs as strings."""
    repo = FileRepository(repo_root)
    mission = build_entity(EntityType.MISSION, {"title": "Mission"})
    assert isinstance(mission, Mission)
    repo.save(mission)
    project = build_entity(EntityType.PROJECT, {"title": "Project", "mission": str(mission.id)})
    assert isinstance(project, Project)
    repo.save(project)
    task = build_entity(EntityType.TASK, {"title": "Task", "project": str(project.id)})
    assert isinstance(task, Task)
    repo.save(task)
    return str(mission.id), str(project.id), str(task.id)
