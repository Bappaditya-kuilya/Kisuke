"""Entity application service.

Thin orchestration over the Storage repository: builds Domain entities from
command parameters, persists them, and reads them back. No business rules live
here beyond the ownership wiring required to construct valid entities.
"""

from __future__ import annotations

from dataclasses import fields, replace
from pathlib import Path
from typing import Any

from kisuke.domain.entities import ENTITY_TYPES, Entity, Project
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import (
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
from kisuke.domain.owner import Owner
from kisuke.domain.timestamp import Timestamp
from kisuke.infrastructure.storage.repository import FOLDER_NAMES, FileRepository

DEFAULT_STATUS: dict[EntityType, Status] = {
    EntityType.MISSION: MissionStatus.ACTIVE,
    EntityType.PROJECT: ProjectStatus.ACTIVE,
    EntityType.TASK: TaskStatus.TODO,
    EntityType.KNOWLEDGE: KnowledgeStatus.ACTIVE,
    EntityType.COOKBOOK: CookbookStatus.ACTIVE,
    EntityType.DECISION: DecisionStatus.PROPOSED,
    EntityType.MEETING: MeetingStatus.SCHEDULED,
    EntityType.PERSON: PersonStatus.ACTIVE,
    EntityType.RESOURCE: ResourceStatus.ACTIVE,
    EntityType.REVIEW: ReviewStatus.PLANNED,
}

ARCHIVED_STATUS: dict[EntityType, Status] = {
    EntityType.MISSION: MissionStatus.ARCHIVED,
    EntityType.PROJECT: ProjectStatus.ARCHIVED,
    EntityType.TASK: TaskStatus.ARCHIVED,
    EntityType.KNOWLEDGE: KnowledgeStatus.ARCHIVED,
    EntityType.COOKBOOK: CookbookStatus.ARCHIVED,
    EntityType.DECISION: DecisionStatus.ARCHIVED,
    EntityType.MEETING: MeetingStatus.ARCHIVED,
    EntityType.PERSON: PersonStatus.ARCHIVED,
    EntityType.RESOURCE: ResourceStatus.ARCHIVED,
    EntityType.REVIEW: ReviewStatus.ARCHIVED,
}


def _to_ids(values: Any) -> list[EntityId]:
    if values is None:
        return []
    items = values if isinstance(values, (list, tuple, set)) else [values]
    ids: list[EntityId] = []
    for item in items:
        if isinstance(item, EntityId):
            ids.append(item)
        elif isinstance(item, str) and item.strip():
            ids.append(EntityId.from_string(item.strip()))
    return ids


def _require_id(value: Any, message: str) -> EntityId:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(message)
    if isinstance(value, EntityId):
        return value
    return EntityId.from_string(str(value).strip())


def _resolve_owner(entity_type: EntityType, params: dict[str, Any]) -> Owner:
    if entity_type in (EntityType.MISSION, EntityType.COOKBOOK):
        return Owner.kisuke_core()
    if entity_type in (EntityType.MEETING, EntityType.PERSON, EntityType.RESOURCE):
        return Owner.independent()
    if entity_type == EntityType.PROJECT:
        return Owner.of(_require_id(params.get("mission"), "project requires --mission <id>"))
    if entity_type in (EntityType.TASK, EntityType.KNOWLEDGE, EntityType.DECISION):
        return Owner.of(
            _require_id(params.get("project"), f"{entity_type} requires --project <id>")
        )
    if entity_type == EntityType.REVIEW:
        return Owner.of(_require_id(params.get("mission"), "review requires --mission <id>"))
    return Owner.independent()


def build_entity(entity_type: EntityType, params: dict[str, Any]) -> Entity:
    """Construct a fully-populated Domain entity from command parameters."""
    now = Timestamp.now()
    cls = ENTITY_TYPES[entity_type]
    base: dict[str, Any] = {
        "id": EntityId.generate(),
        "title": params.get("title") or "",
        "owner": _resolve_owner(entity_type, params),
        "status": DEFAULT_STATUS[entity_type],
        "created_at": now,
        "updated_at": now,
        "tags": list(params.get("tags") or []),
        "references": _to_ids(params.get("references")),
        "attachments": [],
    }
    if entity_type == EntityType.MISSION:
        base.update(
            description=params.get("description") or "",
            priority=params.get("priority"),
            projects=[],
            reviews=[],
        )
    elif entity_type == EntityType.PROJECT:
        base.update(
            description=params.get("description") or "",
            priority=params.get("priority"),
            next_action=None,
            tasks=[],
            knowledge=[],
            decisions=[],
            meetings=[],
            resources=[],
            people=[],
        )
    elif entity_type == EntityType.TASK:
        base.update(
            description=params.get("description") or "",
            priority=params.get("priority"),
            due_date=params.get("due_date"),
            estimated_time=params.get("estimated_time"),
        )
    elif entity_type == EntityType.KNOWLEDGE:
        base.update(
            summary=params.get("summary") or "", content=params.get("content") or "", resources=[]
        )
    elif entity_type == EntityType.COOKBOOK:
        base.update(content=params.get("content") or "", category=params.get("category") or "")
    elif entity_type == EntityType.DECISION:
        base.update(
            decision=params.get("decision") or "",
            reason=params.get("reason") or "",
            alternatives=params.get("alternatives") or "",
        )
    elif entity_type == EntityType.MEETING:
        base.update(
            date=params.get("date") or "",
            people=_to_ids(params.get("people")),
            projects=_to_ids(params.get("projects")),
            tasks=_to_ids(params.get("tasks")),
            decisions=_to_ids(params.get("decisions")),
            resources=_to_ids(params.get("resources")),
            summary=params.get("summary") or "",
        )
    elif entity_type == EntityType.PERSON:
        base.update(
            role=params.get("role") or "",
            organization=params.get("organization") or "",
            email=params.get("email") or "",
            links=list(params.get("links") or []),
            notes=params.get("notes") or "",
        )
    elif entity_type == EntityType.RESOURCE:
        base.update(
            resource_type=params.get("resource_type") or "",
            url=params.get("url") or "",
            description=params.get("description") or "",
        )
    return cls(**base)


def _jsonify(value: Any) -> Any:
    if isinstance(value, EntityId):
        return str(value)
    if isinstance(value, Owner):
        return value.value
    if isinstance(value, list):
        return [_jsonify(item) for item in value]
    if isinstance(value, Timestamp):
        return value.to_datetime().isoformat()
    return value


def entity_to_dict(entity: Entity) -> dict[str, Any]:
    """Return a JSON-serializable mapping of an entity's fields."""
    out: dict[str, Any] = {}
    for field in fields(entity):
        out[field.name] = _jsonify(getattr(entity, field.name))
    out["type"] = entity.entity_type.value
    return out


class EntityService:
    """Repository-backed CRUD for a single entity type's CLI operations."""

    def __init__(self, repo: FileRepository) -> None:
        self.repo = repo

    def create(self, entity_type: EntityType, params: dict[str, Any]) -> Entity:
        entity = build_entity(entity_type, params)
        self.repo.save(entity)
        self._register_in_project(entity_type, entity)
        return entity

    def _register_in_project(self, entity_type: EntityType, entity: Entity) -> None:
        owner_id = entity.owner.entity_id
        if owner_id is None or not self.repo.exists(EntityType.PROJECT, owner_id):
            return
        project = self.repo.load(EntityType.PROJECT, owner_id)
        assert isinstance(project, Project)
        if entity_type == EntityType.TASK and entity.id not in project.tasks:
            self.repo.save(
                replace(project, tasks=project.tasks + [entity.id], updated_at=Timestamp.now())
            )
        elif entity_type == EntityType.KNOWLEDGE and entity.id not in project.knowledge:
            self.repo.save(
                replace(
                    project, knowledge=project.knowledge + [entity.id], updated_at=Timestamp.now()
                )
            )
        elif entity_type == EntityType.DECISION and entity.id not in project.decisions:
            self.repo.save(
                replace(
                    project, decisions=project.decisions + [entity.id], updated_at=Timestamp.now()
                )
            )

    def list(self, entity_type: EntityType) -> list[Entity]:
        return self.repo.all(entity_type)

    def show(self, entity_type: EntityType, entity_id: EntityId) -> Entity:
        return self.repo.load(entity_type, entity_id)

    def archive(self, entity_type: EntityType, entity_id: EntityId) -> Entity:
        entity = self.show(entity_type, entity_id)
        updated = replace(entity, status=ARCHIVED_STATUS[entity_type], updated_at=Timestamp.now())
        self.repo.save(updated)
        return updated

    def path(self, entity_type: EntityType, entity_id: EntityId) -> Path:
        return self.repo.root / FOLDER_NAMES[entity_type] / f"{entity_id}.md"
