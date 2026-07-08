"""Entity <-> Markdown serialization.

Maps each Domain entity to canonical Markdown: a YAML frontmatter block holding
all structured fields, followed by human-readable body sections for prose
fields. The mapping derives directly from docs/architecture/06-data-model.md and
the canonical templates under templates/.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from kisuke.domain.entities import ENTITY_TYPES, Entity
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import STATUS_ENUMS, EntityType
from kisuke.domain.owner import KNOWN_SENTINELS, Owner
from kisuke.domain.timestamp import Timestamp

from .frontmatter import dumps_yaml, join_markdown, loads_yaml, split_markdown

UNIVERSAL_CORE = ["id", "type", "title", "owner", "status"]
TAIL = ["tags", "references", "attachments", "created_at", "updated_at"]

SPECIFIC_FIELDS: dict[EntityType, list[str]] = {
    EntityType.MISSION: ["priority", "projects", "reviews"],
    EntityType.PROJECT: [
        "priority", "next_action", "tasks", "knowledge",
        "decisions", "meetings", "resources", "people",
    ],
    EntityType.TASK: ["priority", "due_date", "estimated_time"],
    EntityType.KNOWLEDGE: ["resources"],
    EntityType.COOKBOOK: ["category"],
    EntityType.DECISION: [],
    EntityType.MEETING: ["date", "people", "projects", "tasks", "decisions", "resources"],
    EntityType.PERSON: ["role", "organization", "email", "links"],
    EntityType.RESOURCE: ["resource_type", "url"],
    EntityType.REVIEW: [
        "review_type", "date", "completed_projects", "blocked_projects", "next_actions",
    ],
    EntityType.ATTACHMENT: ["filename", "mime_type", "size", "checksum"],
}

BODY_SECTIONS: dict[EntityType, list[tuple[str, str]]] = {
    EntityType.MISSION: [("description", "Objective")],
    EntityType.PROJECT: [("description", "Goal")],
    EntityType.TASK: [("description", "Description")],
    EntityType.KNOWLEDGE: [("summary", "Summary"), ("content", "Content")],
    EntityType.COOKBOOK: [("content", "Content")],
    EntityType.DECISION: [
        ("decision", "Decision"),
        ("reason", "Reason"),
        ("alternatives", "Alternatives"),
    ],
    EntityType.MEETING: [("summary", "Summary")],
    EntityType.PERSON: [("notes", "Notes")],
    EntityType.RESOURCE: [("description", "Description")],
    EntityType.REVIEW: [("summary", "Summary")],
    EntityType.ATTACHMENT: [],
}

ID_LIST_FIELDS = {
    "projects", "reviews", "tasks", "knowledge", "decisions", "meetings",
    "resources", "people", "next_actions", "completed_projects",
    "blocked_projects", "references", "attachments",
}

FRONT_FIELDS: dict[EntityType, list[str]] = {
    et: UNIVERSAL_CORE + SPECIFIC_FIELDS[et] + TAIL for et in EntityType
}


def _owner_to_str(owner: Owner) -> str:
    if owner.is_sentinel:
        return owner.sentinel  # type: ignore[return-value]
    return str(owner.entity_id)


def _field_value(entity: Entity, key: str) -> object:
    if key == "id":
        return str(entity.id)
    if key == "type":
        return entity.entity_type.value
    if key == "owner":
        return _owner_to_str(entity.owner)
    if key == "status":
        return entity.status.value
    if key == "created_at":
        return entity.created_at.to_datetime().isoformat()
    if key == "updated_at":
        return entity.updated_at.to_datetime().isoformat()
    value = getattr(entity, key)
    if value is None:
        return None
    if isinstance(value, EntityId):
        return str(value)
    if isinstance(value, list):
        return [str(v) if isinstance(v, EntityId) else v for v in value]
    return value


def _entity_to_frontmatter(entity: Entity) -> dict[str, object]:
    return {key: _field_value(entity, key) for key in FRONT_FIELDS[entity.entity_type]}


def _entity_to_body(entity: Entity) -> str:
    sections: list[str] = []
    for attr, heading in BODY_SECTIONS.get(entity.entity_type, []):
        value = getattr(entity, attr)
        if isinstance(value, str) and value.strip():
            sections.append(f"# {heading}\n\n{value}\n")
    return "\n".join(sections)


def entity_to_markdown(entity: Entity) -> str:
    fm_text = dumps_yaml(_entity_to_frontmatter(entity))
    return join_markdown(fm_text, _entity_to_body(entity))


def _owner_from_str(value: str) -> Owner:
    if value in KNOWN_SENTINELS:
        return Owner(value)
    return Owner.of(EntityId.from_string(value))


def _deserialize_field(et: EntityType, key: str, raw: Any) -> Any:
    if key in ID_LIST_FIELDS:
        return [EntityId.from_string(s) for s in (raw or [])]
    if key in ("tags", "links"):
        return list(raw or [])
    if key == "next_action":
        return EntityId.from_string(raw) if raw else None
    return raw


def _frontmatter_to_kwargs(et: EntityType, fm: dict[str, Any]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    for key in FRONT_FIELDS[et]:
        if key in ("id", "type", "owner", "status", "created_at", "updated_at"):
            continue
        kwargs[key] = _deserialize_field(et, key, fm.get(key))
    id_value = fm["id"]
    assert isinstance(id_value, str)
    kwargs["id"] = EntityId.from_string(id_value)
    title = fm["title"]
    assert isinstance(title, str)
    kwargs["title"] = title
    owner = fm["owner"]
    assert isinstance(owner, str)
    kwargs["owner"] = _owner_from_str(owner)
    enum_cls = STATUS_ENUMS[et]
    status = fm["status"]
    assert isinstance(status, str)
    kwargs["status"] = enum_cls(status)
    created = fm["created_at"]
    updated = fm["updated_at"]
    assert isinstance(created, str) and isinstance(updated, str)
    kwargs["created_at"] = Timestamp.from_datetime(datetime.fromisoformat(created))
    kwargs["updated_at"] = Timestamp.from_datetime(datetime.fromisoformat(updated))
    return kwargs


def _parse_body(body: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("# "):
            if current is not None:
                result[current] = "\n".join(buf).strip()
            current = line[2:].strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        result[current] = "\n".join(buf).strip()
    return result


def _body_to_kwargs(et: EntityType, body_map: dict[str, str]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    for attr, heading in BODY_SECTIONS.get(et, []):
        kwargs[attr] = body_map.get(heading, "")
    return kwargs


def markdown_to_entity(text: str, expected_type: EntityType | None = None) -> Entity:
    fm_text, body = split_markdown(text)
    fm = loads_yaml(fm_text)
    if "type" not in fm:
        raise ValueError("Frontmatter is missing 'type'")
    type_value = fm["type"]
    assert isinstance(type_value, str)
    et = EntityType(type_value)
    if expected_type is not None and et != expected_type:
        raise ValueError(f"Expected {expected_type}, found {et}")
    cls = ENTITY_TYPES[et]
    kwargs = _frontmatter_to_kwargs(et, fm)
    kwargs.update(_body_to_kwargs(et, _parse_body(body)))
    return cls(**kwargs)
