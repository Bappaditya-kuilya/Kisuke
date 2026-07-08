"""Tests for the file-backed Markdown repository.

Covers file-naming strategy, one-entity-per-file, atomic writes, validation
gating, CRUD operations, and UTF-8 persistence.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kisuke.domain.entities import Mission, Project, Task
from kisuke.domain.exceptions import ValidationError
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import MissionStatus, ProjectStatus, TaskStatus
from kisuke.domain.owner import Owner
from kisuke.infrastructure.storage.interfaces import EntityRepository
from kisuke.infrastructure.storage.repository import FOLDER_NAMES, FileRepository
from kisuke.infrastructure.storage.serializer import (
    entity_to_markdown,
)

from .conftest import (
    ATTACHMENT_ID,
    PROJECT_ID,
    TASK_ID,
    TS,
    make_all,
)


def test_repository_implements_interface() -> None:
    assert issubclass(FileRepository, EntityRepository)


def test_save_uses_entity_id_filename(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    mission = next(e for e in make_all() if e.entity_type.value == "mission")
    repo.save(mission)
    expected = tmp_path / "missions" / f"{mission.id}.md"
    assert expected.exists()
    assert expected.read_text(encoding="utf-8") == entity_to_markdown(mission)


def test_one_entity_per_file(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    for entity in make_all():
        repo.save(entity)
    total_md = sum(len(list((tmp_path / folder).glob("*.md"))) for folder in FOLDER_NAMES.values())
    assert total_md == 11


def test_folder_names_match_data_model() -> None:
    assert FOLDER_NAMES["mission"] == "missions"
    assert FOLDER_NAMES["project"] == "projects"
    assert FOLDER_NAMES["task"] == "tasks"
    assert FOLDER_NAMES["knowledge"] == "knowledge"
    assert FOLDER_NAMES["cookbook"] == "cookbook"
    assert FOLDER_NAMES["decision"] == "decisions"
    assert FOLDER_NAMES["meeting"] == "meetings"
    assert FOLDER_NAMES["person"] == "people"
    assert FOLDER_NAMES["resource"] == "resources"
    assert FOLDER_NAMES["review"] == "reviews"
    assert FOLDER_NAMES["attachment"] == "attachments"


def test_load_returns_equal_entity(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    project = next(e for e in make_all() if e.entity_type.value == "project")
    repo.save(project)
    loaded = repo.load(project.entity_type, project.id)
    assert loaded == project


def test_save_overwrites_same_id_file(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    mission = next(e for e in make_all() if e.entity_type.value == "mission")
    repo.save(mission)
    first = list((tmp_path / "missions").glob("*.md"))
    assert len(first) == 1
    repo.save(mission)
    second = list((tmp_path / "missions").glob("*.md"))
    assert len(second) == 1


def test_exists(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    mission = next(e for e in make_all() if e.entity_type.value == "mission")
    assert not repo.exists(mission.entity_type, mission.id)
    repo.save(mission)
    assert repo.exists(mission.entity_type, mission.id)


def test_load_missing_raises(tmp_path: Path) -> None:
    from kisuke.infrastructure.storage.interfaces import RepositoryError

    repo = FileRepository(tmp_path)
    with pytest.raises(RepositoryError):
        repo.load("mission", EntityId.from_string("11111111-1111-1111-1111-111111111111"))


def test_delete(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    mission = next(e for e in make_all() if e.entity_type.value == "mission")
    repo.save(mission)
    assert repo.exists(mission.entity_type, mission.id)
    repo.delete(mission.entity_type, mission.id)
    assert not repo.exists(mission.entity_type, mission.id)


def test_all_sorted_by_id(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    low = EntityId.from_string("00000000-0000-0000-0000-00000000000a")
    high = EntityId.from_string("00000000-0000-0000-0000-00000000000b")
    repo.save(_mission(low, "A"))
    repo.save(_mission(high, "B"))
    result = repo.all("mission")
    assert [e.id for e in result] == [low, high]


def test_atomic_write_leaves_no_temp_files(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    for entity in make_all():
        repo.save(entity)
    temps = list(tmp_path.rglob("*.tmp"))
    assert temps == []


def test_save_rejects_invalid_entity(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    # A Mission must be owned by the kisuke-core sentinel, not an entity id.
    invalid = Mission(
        id=EntityId.from_string("11111111-1111-1111-1111-111111111111"),
        title="Bad",
        owner=Owner.of(PROJECT_ID),
        status=MissionStatus.ACTIVE,
        created_at=TS,
        updated_at=TS,
    )
    with pytest.raises(ValidationError):
        repo.save(invalid)


def test_validate_repository_passes_for_valid_set(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    for entity in make_all():
        repo.save(entity)
    repo.validate_repository()  # must not raise


def test_validate_repository_fails_on_broken_ownership(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    # Project owned by a Task id (wrong owner type) is invalid within a collection.
    bad_project = Project(
        id=PROJECT_ID,
        title="Bad",
        owner=Owner.of(TASK_ID),
        status=ProjectStatus.ACTIVE,
        created_at=TS,
        updated_at=TS,
    )
    repo.save(bad_project)
    with pytest.raises(ValidationError):
        repo.validate_repository()


def test_load_by_id_finds_across_types(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    for entity in make_all():
        repo.save(entity)
    loaded = repo.load_by_id(TASK_ID)
    assert loaded.entity_type.value == "task"
    loaded = repo.load_by_id(ATTACHMENT_ID)
    assert loaded.entity_type.value == "attachment"


def test_load_by_id_missing_raises(tmp_path: Path) -> None:
    from kisuke.infrastructure.storage.interfaces import RepositoryError

    repo = FileRepository(tmp_path)
    with pytest.raises(RepositoryError):
        repo.load_by_id(EntityId.from_string("ffffffff-ffff-ffff-ffff-ffffffffffff"))


def test_utf8_persistence_roundtrip(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    task = Task(
        id=TASK_ID,
        title="日本語 — café",
        owner=Owner.of(PROJECT_ID),
        status=TaskStatus.TODO,
        description="ünïçödé ✓",
        created_at=TS,
        updated_at=TS,
    )
    repo.save(task)
    raw = (tmp_path / "tasks" / f"{TASK_ID}.md").read_text(encoding="utf-8")
    assert "日本語 — café" in raw
    assert "ünïçödé ✓" in raw
    assert repo.load("task", TASK_ID) == task


def _mission(entity_id: EntityId, title: str) -> Mission:
    return Mission(
        id=entity_id,
        title=title,
        owner=Owner.kisuke_core(),
        status=MissionStatus.PLANNING,
        created_at=TS,
        updated_at=TS,
    )
