"""Test factories for the Domain layer.

Builds deterministic entities for tests. Not part of the shipped package.
"""

from __future__ import annotations

from datetime import UTC, datetime

from kisuke.domain.entities import (
    Attachment,
    Cookbook,
    Decision,
    Knowledge,
    Meeting,
    Mission,
    Person,
    Project,
    Resource,
    Review,
    Task,
)
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import (
    AttachmentStatus,
    CookbookStatus,
    DecisionStatus,
    KnowledgeStatus,
    MeetingStatus,
    MissionStatus,
    PersonStatus,
    ProjectStatus,
    ResourceStatus,
    ReviewStatus,
    TaskStatus,
)
from kisuke.domain.owner import Owner
from kisuke.domain.timestamp import Timestamp

TS = Timestamp.from_datetime(datetime(2024, 1, 1, tzinfo=UTC))


def mid(n: int) -> EntityId:
    return EntityId.from_string(f"00000000-0000-0000-0000-{n:012d}")


def make_mission(id: EntityId = mid(1), owner: Owner = Owner.kisuke_core(),
                 status: MissionStatus = MissionStatus.PLANNING) -> Mission:
    return Mission(id=id, title="Mission", owner=owner, status=status, created_at=TS, updated_at=TS)


def make_project(id: EntityId = mid(2), owner: Owner | None = None,
                 status: ProjectStatus = ProjectStatus.PLANNING) -> Project:
    return Project(id=id, title="Project", owner=owner or Owner.of(mid(1)), status=status,
                   created_at=TS, updated_at=TS)


def make_task(id: EntityId = mid(3), owner: Owner | None = None,
              status: TaskStatus = TaskStatus.TODO) -> Task:
    return Task(id=id, title="Task", owner=owner or Owner.of(mid(2)), status=status,
                created_at=TS, updated_at=TS)


def make_knowledge(id: EntityId = mid(4), owner: Owner | None = None,
                  status: KnowledgeStatus = KnowledgeStatus.DRAFT,
                  resources: list[EntityId] | None = None) -> Knowledge:
    return Knowledge(id=id, title="Knowledge", owner=owner or Owner.of(mid(2)), status=status,
                     resources=resources or [], created_at=TS, updated_at=TS)


def make_cookbook(id: EntityId = mid(5), owner: Owner = Owner.kisuke_core(),
                  status: CookbookStatus = CookbookStatus.ACTIVE) -> Cookbook:
    return Cookbook(
        id=id, title="Cookbook", owner=owner, status=status, created_at=TS, updated_at=TS
    )


def make_decision(id: EntityId = mid(6), owner: Owner | None = None,
                  status: DecisionStatus = DecisionStatus.PROPOSED) -> Decision:
    return Decision(id=id, title="Decision", owner=owner or Owner.of(mid(2)), status=status,
                    created_at=TS, updated_at=TS)


def make_meeting(id: EntityId = mid(7), owner: Owner = Owner.independent(),
                 status: MeetingStatus = MeetingStatus.SCHEDULED) -> Meeting:
    return Meeting(id=id, title="Meeting", owner=owner, status=status, created_at=TS, updated_at=TS)


def make_person(id: EntityId = mid(8), owner: Owner = Owner.independent(),
                status: PersonStatus = PersonStatus.ACTIVE) -> Person:
    return Person(id=id, title="Person", owner=owner, status=status, created_at=TS, updated_at=TS)


def make_resource(id: EntityId = mid(9), owner: Owner = Owner.independent(),
                  status: ResourceStatus = ResourceStatus.ACTIVE) -> Resource:
    return Resource(
        id=id, title="Resource", owner=owner, status=status, created_at=TS, updated_at=TS
    )


def make_review(id: EntityId = mid(10), owner: Owner | None = None,
                status: ReviewStatus = ReviewStatus.PLANNED) -> Review:
    return Review(id=id, title="Review", owner=owner or Owner.of(mid(1)), status=status,
                  created_at=TS, updated_at=TS)


def make_attachment(id: EntityId = mid(11), owner: Owner | None = None,
                    status: AttachmentStatus = AttachmentStatus.ACTIVE) -> Attachment:
    return Attachment(id=id, title="Attachment", owner=owner or Owner.of(mid(2)), status=status,
                      created_at=TS, updated_at=TS)
