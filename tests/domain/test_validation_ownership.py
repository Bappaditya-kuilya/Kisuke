from __future__ import annotations

import pytest

from kisuke.domain.exceptions import IdentityError, OwnershipError
from kisuke.domain.owner import Owner
from kisuke.domain.validation import validate_entities, validate_entity
from tests.domain.factories import (
    make_attachment,
    make_mission,
    make_person,
    make_project,
    make_task,
    mid,
)


def test_mission_sentinel_owner_valid() -> None:
    validate_entity(make_mission())
    validate_entities([make_mission()])


def test_project_owned_by_mission_valid() -> None:
    mission = make_mission()
    project = make_project(owner=Owner.of(mission.id))
    validate_entities([mission, project])


def test_project_with_sentinel_owner_rejected() -> None:
    with pytest.raises(OwnershipError):
        validate_entity(make_project(owner=Owner.independent()))


def test_mission_with_entity_owner_rejected() -> None:
    with pytest.raises(OwnershipError):
        validate_entity(make_mission(owner=Owner.of(mid(2))))


def test_task_with_sentinel_owner_rejected() -> None:
    with pytest.raises(OwnershipError):
        validate_entity(make_task(owner=Owner.kisuke_core()))


def test_missing_owner_target_rejected() -> None:
    project = make_project(owner=Owner.of(mid(500)))
    with pytest.raises(OwnershipError):
        validate_entities([project])


def test_wrong_owner_type_rejected() -> None:
    person = make_person()
    project = make_project(owner=Owner.of(person.id))
    with pytest.raises(OwnershipError):
        validate_entities([person, project])


def test_attachment_owned_by_any_entity_valid() -> None:
    mission = make_mission()
    project = make_project(owner=Owner.of(mission.id))
    attachment = make_attachment(owner=Owner.of(project.id))
    validate_entities([mission, project, attachment])


def test_attachment_missing_owner_rejected() -> None:
    attachment = make_attachment(owner=Owner.of(mid(777)))
    with pytest.raises(OwnershipError):
        validate_entities([attachment])


def test_duplicate_entity_id_rejected() -> None:
    mission = make_mission()
    with pytest.raises(IdentityError):
        validate_entities([mission, mission])
