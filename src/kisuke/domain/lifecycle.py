"""Entity types and lifecycle status enums.

Each entity has a fixed set of lifecycle states defined by the Domain Model.
Status values are ``StrEnum`` members so their string form matches the Data
Model exactly.
"""

from __future__ import annotations

from enum import StrEnum


class EntityType(StrEnum):
    MISSION = "mission"
    PROJECT = "project"
    TASK = "task"
    KNOWLEDGE = "knowledge"
    COOKBOOK = "cookbook"
    DECISION = "decision"
    MEETING = "meeting"
    PERSON = "person"
    RESOURCE = "resource"
    REVIEW = "review"
    ATTACHMENT = "attachment"


class MissionStatus(StrEnum):
    PLANNING = "Planning"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class ProjectStatus(StrEnum):
    PLANNING = "Planning"
    ACTIVE = "Active"
    BLOCKED = "Blocked"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class TaskStatus(StrEnum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    ARCHIVED = "Archived"


class KnowledgeStatus(StrEnum):
    DRAFT = "Draft"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    ARCHIVED = "Archived"


class CookbookStatus(StrEnum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class DecisionStatus(StrEnum):
    PROPOSED = "Proposed"
    ACCEPTED = "Accepted"
    SUPERSEDED = "Superseded"
    ARCHIVED = "Archived"


class MeetingStatus(StrEnum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class PersonStatus(StrEnum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class ResourceStatus(StrEnum):
    ACTIVE = "Active"
    UNAVAILABLE = "Unavailable"
    ARCHIVED = "Archived"


class ReviewStatus(StrEnum):
    PLANNED = "Planned"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class AttachmentStatus(StrEnum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"


STATUS_ENUMS: dict[EntityType, type[StrEnum]] = {
    EntityType.MISSION: MissionStatus,
    EntityType.PROJECT: ProjectStatus,
    EntityType.TASK: TaskStatus,
    EntityType.KNOWLEDGE: KnowledgeStatus,
    EntityType.COOKBOOK: CookbookStatus,
    EntityType.DECISION: DecisionStatus,
    EntityType.MEETING: MeetingStatus,
    EntityType.PERSON: PersonStatus,
    EntityType.RESOURCE: ResourceStatus,
    EntityType.REVIEW: ReviewStatus,
    EntityType.ATTACHMENT: AttachmentStatus,
}

Status = (
    MissionStatus
    | ProjectStatus
    | TaskStatus
    | KnowledgeStatus
    | CookbookStatus
    | DecisionStatus
    | MeetingStatus
    | PersonStatus
    | ResourceStatus
    | ReviewStatus
    | AttachmentStatus
)
