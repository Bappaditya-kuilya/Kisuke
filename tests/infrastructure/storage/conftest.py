"""Shared test fixtures for the Storage layer.

Builds fully-populated, structurally-valid entities of every Domain type so that
round-trip, golden-file, and repository tests operate on realistic data.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from kisuke.domain.entities import (
    Attachment,
    Cookbook,
    Decision,
    Entity,
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
    EntityType,
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

TS = Timestamp.from_datetime(datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC))


def eid(seed: str) -> EntityId:
    return EntityId.from_string(f"{seed:0<32}")


MISSION_ID = eid("1000000000000000000000000000000")
PROJECT_ID = eid("2000000000000000000000000000000")
TASK_ID = eid("3000000000000000000000000000000")
KNOWLEDGE_ID = eid("4000000000000000000000000000000")
COOKBOOK_ID = eid("5000000000000000000000000000000")
DECISION_ID = eid("6000000000000000000000000000000")
MEETING_ID = eid("7000000000000000000000000000000")
PERSON_ID = eid("8000000000000000000000000000000")
RESOURCE_ID = eid("9000000000000000000000000000000")
REVIEW_ID = eid("a000000000000000000000000000000")
ATTACHMENT_ID = eid("b000000000000000000000000000000")


def make_all() -> list[Entity]:
    return [
        Mission(
            id=MISSION_ID,
            title="Become an AI Engineer",
            owner=Owner.kisuke_core(),
            status=MissionStatus.ACTIVE,
            description="Long-term career objective.",
            priority="high",
            projects=[PROJECT_ID],
            reviews=[REVIEW_ID],
            tags=["career"],
            references=[REVIEW_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Project(
            id=PROJECT_ID,
            title="Build Kisuke",
            owner=Owner.of(MISSION_ID),
            status=ProjectStatus.ACTIVE,
            description="Local-first context engine.",
            priority="high",
            next_action=TASK_ID,
            tasks=[TASK_ID],
            knowledge=[KNOWLEDGE_ID],
            decisions=[DECISION_ID],
            meetings=[MEETING_ID],
            resources=[RESOURCE_ID],
            people=[PERSON_ID],
            tags=["core"],
            references=[MISSION_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Task(
            id=TASK_ID,
            title="Implement parser",
            owner=Owner.of(PROJECT_ID),
            status=TaskStatus.IN_PROGRESS,
            description="Parse frontmatter.",
            priority="medium",
            due_date="2024-02-01",
            estimated_time="3h",
            tags=["parser"],
            references=[RESOURCE_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Knowledge(
            id=KNOWLEDGE_ID,
            title="SQLite indexing notes",
            owner=Owner.of(PROJECT_ID),
            status=KnowledgeStatus.ACTIVE,
            summary="How FTS5 works.",
            content="Full text search details.",
            resources=[RESOURCE_ID],
            tags=["db"],
            references=[RESOURCE_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Cookbook(
            id=COOKBOOK_ID,
            title="Git commands",
            owner=Owner.kisuke_core(),
            status=CookbookStatus.ACTIVE,
            content="git rebase --onto",
            category="vcs",
            tags=["git"],
            references=[RESOURCE_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Decision(
            id=DECISION_ID,
            title="Use Markdown source of truth",
            owner=Owner.of(PROJECT_ID),
            status=DecisionStatus.ACCEPTED,
            decision="Markdown is canonical.",
            reason="Portable and version controlled.",
            alternatives="JSON or SQLite blobs.",
            tags=["storage"],
            references=[RESOURCE_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Meeting(
            id=MEETING_ID,
            title="Weekly sync",
            owner=Owner.independent(),
            status=MeetingStatus.COMPLETED,
            date="2024-01-08",
            people=[PERSON_ID],
            projects=[PROJECT_ID],
            tasks=[TASK_ID],
            decisions=[DECISION_ID],
            resources=[RESOURCE_ID],
            summary="Discussed roadmap.",
            tags=["sync"],
            references=[PROJECT_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Person(
            id=PERSON_ID,
            title="Ada Mentor",
            owner=Owner.independent(),
            status=PersonStatus.ACTIVE,
            role="Mentor",
            organization="University",
            email="ada@example.com",
            links=["https://example.com"],
            notes="Weekly mentor.",
            tags=["people"],
            references=[MEETING_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Resource(
            id=RESOURCE_ID,
            title="SQLite docs",
            owner=Owner.independent(),
            status=ResourceStatus.ACTIVE,
            resource_type="Documentation",
            url="https://sqlite.org/docs",
            description="Official reference.",
            tags=["docs"],
            references=[KNOWLEDGE_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Review(
            id=REVIEW_ID,
            title="Weekly review",
            owner=Owner.of(MISSION_ID),
            status=ReviewStatus.COMPLETED,
            review_type="Weekly",
            date="2024-01-07",
            summary="Good progress.",
            completed_projects=[PROJECT_ID],
            blocked_projects=[],
            next_actions=[TASK_ID],
            tags=["review"],
            references=[MISSION_ID],
            attachments=[ATTACHMENT_ID],
            created_at=TS,
            updated_at=TS,
        ),
        Attachment(
            id=ATTACHMENT_ID,
            title="architecture.png",
            owner=Owner.of(PROJECT_ID),
            status=AttachmentStatus.ACTIVE,
            filename="architecture.png",
            mime_type="image/png",
            size=2048,
            checksum="deadbeef",
            tags=["asset"],
            references=[],
            attachments=[],
            created_at=TS,
            updated_at=TS,
        ),
    ]


@pytest.fixture
def entities() -> list[Entity]:
    return make_all()


@pytest.fixture
def entity_by_type() -> dict[EntityType, Entity]:
    return {e.entity_type: e for e in make_all()}
