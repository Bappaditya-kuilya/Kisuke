from __future__ import annotations

import pytest

from kisuke.domain.entities import Meeting, Project
from kisuke.domain.exceptions import RelationshipError
from kisuke.domain.owner import Owner
from kisuke.domain.validation import validate_entities
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


def _project(**fields: object) -> Project:
    base = dict(make_project().__dict__)
    base.update(fields)
    return Project(**base)


def _meeting(**fields: object) -> Meeting:
    base = dict(make_meeting().__dict__)
    base.update(fields)
    return Meeting(**base)


def test_missing_reference_rejected() -> None:
    mission = make_mission()
    project = _project(tasks=[mid(999)])
    with pytest.raises(RelationshipError):
        validate_entities([mission, project])


def test_disallowed_reference_type_rejected() -> None:
    mission = make_mission()
    person = make_person()
    project = _project(tasks=[person.id])
    with pytest.raises(RelationshipError):
        validate_entities([mission, person, project])


def test_duplicate_reference_rejected() -> None:
    mission = make_mission()
    project = _project(tasks=[mid(3), mid(3)])
    with pytest.raises(RelationshipError):
        validate_entities([mission, project])


def test_attachment_must_reference_attachment() -> None:
    mission = make_mission()
    project = make_project(owner=Owner.of(mission.id))
    task = make_task(owner=Owner.of(project.id))
    project = _project(owner=Owner.of(mission.id), attachments=[task.id])
    with pytest.raises(RelationshipError):
        validate_entities([mission, project, task])


def test_generic_references_allow_any_type() -> None:
    mission = make_mission()
    person = make_person()
    project = _project(references=[person.id])
    validate_entities([mission, person, project])


def test_next_action_wrong_type_rejected() -> None:
    mission = make_mission()
    project = _project(next_action=mission.id)
    with pytest.raises(RelationshipError):
        validate_entities([mission, project])


def test_next_action_missing_rejected() -> None:
    mission = make_mission()
    project = _project(next_action=mid(123))
    with pytest.raises(RelationshipError):
        validate_entities([mission, project])


def test_meeting_project_reference_valid() -> None:
    mission = make_mission()
    project = make_project()
    meeting = _meeting(projects=[project.id])
    validate_entities([mission, project, meeting])


def test_meeting_disallowed_reference_rejected() -> None:
    mission = make_mission()
    project = make_project(owner=Owner.of(mission.id))
    task = make_task(owner=Owner.of(project.id))
    meeting = _meeting(projects=[task.id])
    with pytest.raises(RelationshipError):
        validate_entities([mission, project, task, meeting])


def test_valid_full_graph_passes() -> None:
    mission = make_mission()
    project = make_project(owner=Owner.of(mission.id))
    task = make_task(owner=Owner.of(project.id))
    knowledge = make_knowledge(owner=Owner.of(project.id))
    cookbook = make_cookbook()
    decision = make_decision(owner=Owner.of(project.id))
    meeting = _meeting(projects=[project.id], tasks=[task.id], people=[make_person().id])
    person = make_person()
    resource = make_resource()
    review = make_review(owner=Owner.of(mission.id))
    attachment = make_attachment(owner=Owner.of(project.id))

    project = _project(
        owner=Owner.of(mission.id),
        tasks=[task.id], knowledge=[knowledge.id], decisions=[decision.id],
        meetings=[meeting.id], resources=[resource.id], people=[person.id],
        next_action=task.id,
    )
    meeting = _meeting(projects=[project.id], tasks=[task.id], people=[person.id])
    knowledge = make_knowledge(owner=Owner.of(project.id), resources=[resource.id])

    validate_entities([
        mission, project, task, knowledge, cookbook, decision,
        meeting, person, resource, review, attachment,
    ])
