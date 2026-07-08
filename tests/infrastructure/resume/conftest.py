"""Shared fixtures for Resume-layer tests."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest

from kisuke.domain.entities import (
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
from kisuke.infrastructure.storage.repository import FileRepository

TS = Timestamp.from_datetime(datetime(2024, 1, 1, tzinfo=UTC))

M = "11111111-1111-1111-1111-111111111111"
P = "22222222-2222-2222-2222-222222222222"
T1 = "33333333-3333-3333-3333-333333333333"
T2 = "44444444-4444-4444-4444-444444444444"
P2 = "22222222-2222-2222-2222-222222222223"
K = "55555555-5555-5555-5555-555555555555"
D = "66666666-6666-6666-6666-666666666666"
MTG = "77777777-7777-7777-7777-777777777777"
MTG2 = "77777777-7777-7777-7777-777777777778"
R = "88888888-8888-8888-8888-888888888888"
PERS = "99999999-9999-9999-9999-999999999999"
REV = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


@pytest.fixture
def working_repo(tmp_path: Path) -> Path:
    repo = FileRepository(tmp_path)
    mission = Mission(
        id=EntityId.from_string(M),
        title="Become an AI Engineer",
        owner=Owner.kisuke_core(),
        status=MissionStatus.ACTIVE,
        projects=[EntityId.from_string(P), EntityId.from_string(P2)],
        reviews=[EntityId.from_string(REV)],
        created_at=TS,
        updated_at=TS,
    )
    project = Project(
        id=EntityId.from_string(P),
        title="Build Kisuke Platform",
        owner=Owner.of(EntityId.from_string(M)),
        status=ProjectStatus.ACTIVE,
        tasks=[EntityId.from_string(T1), EntityId.from_string(T2)],
        knowledge=[EntityId.from_string(K)],
        decisions=[EntityId.from_string(D)],
        meetings=[EntityId.from_string(MTG)],
        resources=[EntityId.from_string(R)],
        people=[EntityId.from_string(PERS)],
        next_action=EntityId.from_string(T1),
        created_at=TS,
        updated_at=TS,
    )
    project2 = Project(
        id=EntityId.from_string(P2),
        title="Side Project",
        owner=Owner.of(EntityId.from_string(M)),
        status=ProjectStatus.ACTIVE,
        created_at=TS,
        updated_at=TS,
    )
    task1 = Task(
        id=EntityId.from_string(T1),
        title="Implement parser",
        owner=Owner.of(EntityId.from_string(P)),
        status=TaskStatus.IN_PROGRESS,
        references=[EntityId.from_string(R)],
        created_at=TS,
        updated_at=TS,
    )
    task2 = Task(
        id=EntityId.from_string(T2),
        title="Write docs",
        owner=Owner.of(EntityId.from_string(P)),
        status=TaskStatus.TODO,
        created_at=TS,
        updated_at=TS,
    )
    knowledge = Knowledge(
        id=EntityId.from_string(K),
        title="SQLite notes",
        owner=Owner.of(EntityId.from_string(P)),
        status=KnowledgeStatus.ACTIVE,
        resources=[EntityId.from_string(R)],
        created_at=TS,
        updated_at=TS,
    )
    decision = Decision(
        id=EntityId.from_string(D),
        title="Use Markdown",
        owner=Owner.of(EntityId.from_string(P)),
        status=DecisionStatus.ACCEPTED,
        created_at=TS,
        updated_at=TS,
    )
    meeting = Meeting(
        id=EntityId.from_string(MTG),
        title="Weekly sync",
        owner=Owner.independent(),
        status=MeetingStatus.COMPLETED,
        projects=[EntityId.from_string(P)],
        people=[EntityId.from_string(PERS)],
        created_at=TS,
        updated_at=TS,
    )
    meeting2 = Meeting(
        id=EntityId.from_string(MTG2),
        title="Ad-hoc",
        owner=Owner.independent(),
        status=MeetingStatus.COMPLETED,
        projects=[EntityId.from_string(P)],
        people=[],
        created_at=TS,
        updated_at=TS,
    )
    resource = Resource(
        id=EntityId.from_string(R),
        title="SQLite docs",
        owner=Owner.independent(),
        status=ResourceStatus.ACTIVE,
        created_at=TS,
        updated_at=TS,
    )
    person = Person(
        id=EntityId.from_string(PERS),
        title="Ada Mentor",
        owner=Owner.independent(),
        status=PersonStatus.ACTIVE,
        created_at=TS,
        updated_at=TS,
    )
    review = Review(
        id=EntityId.from_string(REV),
        title="Weekly review",
        owner=Owner.of(EntityId.from_string(M)),
        status=ReviewStatus.COMPLETED,
        review_type="Weekly",
        date="2024-01-07",
        created_at=TS,
        updated_at=TS,
    )
    for entity in (
        mission,
        project,
        project2,
        task1,
        task2,
        knowledge,
        decision,
        meeting,
        meeting2,
        resource,
        person,
        review,
    ):
        repo.save(entity)
    return tmp_path


def make_bench_repo(tmp_path: Path, n: int = 150) -> Path:
    repo = FileRepository(tmp_path)
    mission = Mission(
        id=EntityId.from_string(str(uuid.UUID(int=1))),
        title="Bench Mission",
        owner=Owner.kisuke_core(),
        status=MissionStatus.ACTIVE,
        created_at=TS,
        updated_at=TS,
    )
    task_ids = [EntityId.from_string(str(uuid.UUID(int=1000 + i))) for i in range(n)]
    project = Project(
        id=EntityId.from_string(str(uuid.UUID(int=2))),
        title="Bench Project",
        owner=Owner.of(mission.id),
        status=ProjectStatus.ACTIVE,
        tasks=task_ids,
        created_at=TS,
        updated_at=TS,
    )
    repo.save(mission)
    repo.save(project)
    for task_id in task_ids:
        repo.save(
            Task(
                id=task_id,
                title=f"Bench task number {task_id}",
                owner=Owner.of(project.id),
                status=TaskStatus.TODO,
                created_at=TS,
                updated_at=TS,
            )
        )
    return tmp_path


@pytest.fixture
def bench_repo(tmp_path: Path) -> Path:
    return make_bench_repo(tmp_path, 150)
