from __future__ import annotations

from kisuke.domain.entities import (
    ENTITY_TYPES,
    Entity,
    Project,
)
from kisuke.domain.lifecycle import EntityType
from tests.domain.factories import (
    make_attachment,
    make_cookbook,
    make_decision,
    make_knowledge,
    make_meeting,
    make_mission,
    make_person,
    make_project,
    make_resource,
    make_review,
    make_task,
    mid,
)


def test_all_eleven_entity_types_registered() -> None:
    assert len(ENTITY_TYPES) == 11
    assert set(ENTITY_TYPES) == set(EntityType)


def test_entity_type_classvars() -> None:
    assert make_mission().entity_type == EntityType.MISSION
    assert make_project().entity_type == EntityType.PROJECT
    assert make_task().entity_type == EntityType.TASK
    assert make_knowledge().entity_type == EntityType.KNOWLEDGE
    assert make_cookbook().entity_type == EntityType.COOKBOOK
    assert make_decision().entity_type == EntityType.DECISION
    assert make_meeting().entity_type == EntityType.MEETING
    assert make_person().entity_type == EntityType.PERSON
    assert make_resource().entity_type == EntityType.RESOURCE
    assert make_review().entity_type == EntityType.REVIEW
    assert make_attachment().entity_type == EntityType.ATTACHMENT


def test_reference_ids_excludes_tags_and_combines_lists() -> None:
    project = make_project()
    project = Project(**{**project.__dict__, "tasks": [mid(3)], "people": [mid(8)], "tags": ["x"]})
    ids = project.reference_ids()
    assert mid(3) in ids
    assert mid(8) in ids
    assert "x" not in ids


def test_entities_are_frozen() -> None:
    mission = make_mission()
    try:
        mission.title = "changed"  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("Entity was mutable")


def test_entity_is_base_for_all() -> None:
    for entity in (
        make_mission(),
        make_project(),
        make_task(),
        make_knowledge(),
        make_cookbook(),
        make_decision(),
        make_meeting(),
        make_person(),
        make_resource(),
        make_review(),
        make_attachment(),
    ):
        assert isinstance(entity, Entity)
