"""Shared fixtures for Search-layer tests."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest

from kisuke.domain.entities import Mission, Project, Task
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import (
    EntityType,
    MissionStatus,
    ProjectStatus,
    TaskStatus,
)
from kisuke.domain.owner import Owner
from kisuke.domain.timestamp import Timestamp
from kisuke.infrastructure.storage.frontmatter import dumps_yaml, join_markdown
from kisuke.infrastructure.storage.repository import FOLDER_NAMES, FileRepository
from tests.infrastructure.storage.conftest import make_all

TS = Timestamp.from_datetime(datetime(2024, 1, 1, tzinfo=UTC))


def _md(et_value: str, name: str, fm: dict, body: str, root: Path) -> Path:
    folder = FOLDER_NAMES[EntityType(et_value)]
    path = root / folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(join_markdown(dumps_yaml(fm), body), encoding="utf-8")
    return path


def _full(**kw: object) -> dict:
    base = {
        "tags": [], "references": [], "attachments": [],
        "created_at": "2024-01-01T00:00:00+00:00", "updated_at": "2024-01-01T00:00:00+00:00",
    }
    base.update(kw)
    return base


@pytest.fixture
def valid_repo(tmp_path: Path) -> Path:
    repo = FileRepository(tmp_path)
    for entity in make_all():
        repo.save(entity)
    return tmp_path


@pytest.fixture
def filter_repo(tmp_path: Path) -> Path:
    _md("mission", "m1.md", _full(
        id="11111111-1111-1111-1111-111111111111", type="mission",
        title="Alpha shared", owner="kisuke-core", status="Active",
    ), "", tmp_path)
    _md("cookbook", "c1.md", _full(
        id="22222222-2222-2222-2222-222222222222", type="cookbook",
        title="Beta shared", owner="kisuke-core", status="Active",
    ), "", tmp_path)
    _md("person", "p1.md", _full(
        id="33333333-3333-3333-3333-333333333333", type="person",
        title="Gamma shared", owner="independent", status="Active",
    ), "", tmp_path)
    return tmp_path


def make_bench_repo(tmp_path: Path, n: int = 200) -> Path:
    repo = FileRepository(tmp_path)
    mission = Mission(
        id=EntityId.from_string(str(uuid.UUID(int=1))),
        title="Bench Mission", owner=Owner.kisuke_core(),
        status=MissionStatus.ACTIVE, created_at=TS, updated_at=TS,
    )
    project = Project(
        id=EntityId.from_string(str(uuid.UUID(int=2))),
        title="Bench Project", owner=Owner.of(mission.id),
        status=ProjectStatus.ACTIVE, created_at=TS, updated_at=TS,
    )
    repo.save(mission)
    repo.save(project)
    for i in range(n):
        repo.save(Task(
            id=EntityId.from_string(str(uuid.UUID(int=1000 + i))),
            title=f"Bench task number {i} alpha",
            owner=Owner.of(project.id),
            status=TaskStatus.TODO, created_at=TS, updated_at=TS,
        ))
    return tmp_path


@pytest.fixture
def bench_repo(tmp_path: Path) -> Path:
    return make_bench_repo(tmp_path, 200)
