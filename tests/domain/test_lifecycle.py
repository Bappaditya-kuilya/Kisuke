from __future__ import annotations

import pytest

from kisuke.domain.exceptions import LifecycleError, OwnershipError
from kisuke.domain.lifecycle import (
    STATUS_ENUMS,
    EntityType,
    MissionStatus,
    ProjectStatus,
    TaskStatus,
)
from kisuke.domain.owner import Owner
from kisuke.domain.validation import validate_entities, validate_entity, validate_status
from tests.domain.factories import make_mission, make_project, mid


def test_entity_type_values() -> None:
    assert EntityType.MISSION == "mission"
    assert set(EntityType) == {
        EntityType.MISSION, EntityType.PROJECT, EntityType.TASK, EntityType.KNOWLEDGE,
        EntityType.COOKBOOK, EntityType.DECISION, EntityType.MEETING, EntityType.PERSON,
        EntityType.RESOURCE, EntityType.REVIEW, EntityType.ATTACHMENT,
    }


def test_status_enums_map_all_types() -> None:
    assert set(STATUS_ENUMS) == set(EntityType)


def test_status_enum_values() -> None:
    assert MissionStatus.ACTIVE == "Active"
    assert ProjectStatus.BLOCKED == "Blocked"
    assert TaskStatus.IN_PROGRESS == "In Progress"


def test_validate_status_ok() -> None:
    validate_status(EntityType.MISSION, MissionStatus.ACTIVE)


def test_validate_status_invalid_raises() -> None:
    with pytest.raises(LifecycleError):
        validate_status(EntityType.TASK, MissionStatus.ACTIVE)


def test_validate_entity_lifecycle_ok() -> None:
    make_mission()


def test_validate_entity_ownership_structure_ok() -> None:
    make_mission()


def test_project_requires_mission_owner_structure() -> None:
    project = make_project(owner=Owner.independent())
    with pytest.raises(OwnershipError):
        validate_entity(project)


def test_validate_entity_rejects_invalid_status() -> None:
    from kisuke.domain.entities import Mission
    from kisuke.domain.lifecycle import TaskStatus

    bad = Mission(
        id=mid(1), title="M", owner=Owner.kisuke_core(),
        status=TaskStatus.TODO, created_at=make_mission().created_at,
        updated_at=make_mission().updated_at,
    )
    with pytest.raises(LifecycleError):
        validate_entity(bad)


def test_validate_entities_rejects_invalid_status() -> None:
    from kisuke.domain.entities import Mission
    from kisuke.domain.lifecycle import TaskStatus

    bad = Mission(
        id=mid(1), title="M", owner=Owner.kisuke_core(),
        status=TaskStatus.TODO, created_at=make_mission().created_at,
        updated_at=make_mission().updated_at,
    )
    with pytest.raises(LifecycleError):
        validate_entities([bad])
