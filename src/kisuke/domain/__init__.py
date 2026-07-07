"""Kisuke Domain layer.

Pure business logic: entities, value objects, ownership/relationship/lifecycle
rules, and validation. No infrastructure, filesystem, parsing, or AI.
"""

from __future__ import annotations

from .entities import (
    ENTITY_TYPES,
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
from .exceptions import (
    DomainError,
    IdentityError,
    LifecycleError,
    OwnershipError,
    RelationshipError,
    ValidationError,
)
from .ids import EntityId
from .lifecycle import (
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
    Status,
    TaskStatus,
)
from .owner import Owner
from .relationships import OWNERSHIP_RULES, RELATIONSHIP_FIELDS
from .timestamp import Timestamp
from .validation import validate_entities, validate_entity, validate_status

__all__ = [
    "Attachment",
    "Cookbook",
    "Decision",
    "DomainError",
    "Entity",
    "ENTITY_TYPES",
    "EntityId",
    "EntityType",
    "IdentityError",
    "Knowledge",
    "LifecycleError",
    "Meeting",
    "Mission",
    "Owner",
    "OWNERSHIP_RULES",
    "Person",
    "Project",
    "RELATIONSHIP_FIELDS",
    "RelationshipError",
    "Resource",
    "Review",
    "Status",
    "Task",
    "Timestamp",
    "ValidationError",
    "validate_entity",
    "validate_entities",
    "validate_status",
    "AttachmentStatus",
    "CookbookStatus",
    "DecisionStatus",
    "KnowledgeStatus",
    "MeetingStatus",
    "MissionStatus",
    "PersonStatus",
    "ProjectStatus",
    "ResourceStatus",
    "ReviewStatus",
    "TaskStatus",
    "OwnershipError",
]
