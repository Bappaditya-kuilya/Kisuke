"""Domain entities.

Every entity carries the Universal Entity Schema (id, title, owner, status,
created_at, updated_at, optional tags/references/attachments) and adds its own
fields from the Data Model. Entities are immutable frozen dataclasses; they hold
no infrastructure, filesystem, or parsing logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import ClassVar

from .ids import EntityId
from .lifecycle import (
    EntityType,
    Status,
)
from .owner import Owner
from .timestamp import Timestamp


@dataclass(frozen=True)
class Entity:
    """Base for all Kisuke entities (Universal Entity Schema)."""

    id: EntityId
    title: str
    owner: Owner
    status: Status
    created_at: Timestamp
    updated_at: Timestamp
    tags: list[str] = field(default_factory=list)
    references: list[EntityId] = field(default_factory=list)
    attachments: list[EntityId] = field(default_factory=list)

    entity_type: ClassVar[EntityType]

    def reference_ids(self) -> list[EntityId]:
        """All referenced entity IDs held in list-of-ID fields."""
        ids: list[EntityId] = []
        for f in fields(self):
            if f.name == "tags":
                continue
            value = getattr(self, f.name)
            if isinstance(value, list) and value and all(isinstance(v, EntityId) for v in value):
                ids.extend(value)
        return ids


@dataclass(frozen=True)
class Mission(Entity):
    description: str = ""
    priority: str | None = None
    projects: list[EntityId] = field(default_factory=list)
    reviews: list[EntityId] = field(default_factory=list)
    entity_type: ClassVar[EntityType] = EntityType.MISSION


@dataclass(frozen=True)
class Project(Entity):
    description: str = ""
    priority: str | None = None
    next_action: EntityId | None = None
    tasks: list[EntityId] = field(default_factory=list)
    knowledge: list[EntityId] = field(default_factory=list)
    decisions: list[EntityId] = field(default_factory=list)
    meetings: list[EntityId] = field(default_factory=list)
    resources: list[EntityId] = field(default_factory=list)
    people: list[EntityId] = field(default_factory=list)
    entity_type: ClassVar[EntityType] = EntityType.PROJECT


@dataclass(frozen=True)
class Task(Entity):
    description: str = ""
    priority: str | None = None
    due_date: str | None = None
    estimated_time: str | None = None
    entity_type: ClassVar[EntityType] = EntityType.TASK


@dataclass(frozen=True)
class Knowledge(Entity):
    summary: str = ""
    content: str = ""
    resources: list[EntityId] = field(default_factory=list)
    entity_type: ClassVar[EntityType] = EntityType.KNOWLEDGE


@dataclass(frozen=True)
class Cookbook(Entity):
    content: str = ""
    category: str = ""
    entity_type: ClassVar[EntityType] = EntityType.COOKBOOK


@dataclass(frozen=True)
class Decision(Entity):
    decision: str = ""
    reason: str = ""
    alternatives: str = ""
    entity_type: ClassVar[EntityType] = EntityType.DECISION


@dataclass(frozen=True)
class Meeting(Entity):
    date: str = ""
    people: list[EntityId] = field(default_factory=list)
    projects: list[EntityId] = field(default_factory=list)
    tasks: list[EntityId] = field(default_factory=list)
    decisions: list[EntityId] = field(default_factory=list)
    resources: list[EntityId] = field(default_factory=list)
    summary: str = ""
    entity_type: ClassVar[EntityType] = EntityType.MEETING


@dataclass(frozen=True)
class Person(Entity):
    role: str = ""
    organization: str = ""
    email: str = ""
    links: list[str] = field(default_factory=list)
    notes: str = ""
    entity_type: ClassVar[EntityType] = EntityType.PERSON


@dataclass(frozen=True)
class Resource(Entity):
    resource_type: str = ""
    url: str = ""
    description: str = ""
    entity_type: ClassVar[EntityType] = EntityType.RESOURCE


@dataclass(frozen=True)
class Review(Entity):
    review_type: str = ""
    date: str = ""
    summary: str = ""
    completed_projects: list[EntityId] = field(default_factory=list)
    blocked_projects: list[EntityId] = field(default_factory=list)
    next_actions: list[EntityId] = field(default_factory=list)
    entity_type: ClassVar[EntityType] = EntityType.REVIEW


@dataclass(frozen=True)
class Attachment(Entity):
    filename: str = ""
    mime_type: str = ""
    size: int = 0
    checksum: str = ""
    entity_type: ClassVar[EntityType] = EntityType.ATTACHMENT


ENTITY_TYPES: dict[EntityType, type[Entity]] = {
    EntityType.MISSION: Mission,
    EntityType.PROJECT: Project,
    EntityType.TASK: Task,
    EntityType.KNOWLEDGE: Knowledge,
    EntityType.COOKBOOK: Cookbook,
    EntityType.DECISION: Decision,
    EntityType.MEETING: Meeting,
    EntityType.PERSON: Person,
    EntityType.RESOURCE: Resource,
    EntityType.REVIEW: Review,
    EntityType.ATTACHMENT: Attachment,
}
