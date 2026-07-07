"""Ownership and relationship rules for the Domain Model.

Extracted directly from docs/architecture/04-domain-model.md (Ownership Rules,
Relationship Model, Cardinality). These tables are the single source of truth
for ownership and relationship validation; the validator enforces them.
"""

from __future__ import annotations

from dataclasses import dataclass

from .lifecycle import EntityType


@dataclass(frozen=True)
class OwnershipRule:
    """How an entity's owner must be formed."""

    sentinel: str | None = None
    owner_type: EntityType | None = None
    parent: bool = False


OWNERSHIP_RULES: dict[EntityType, OwnershipRule] = {
    EntityType.MISSION: OwnershipRule(sentinel="kisuke-core"),
    EntityType.COOKBOOK: OwnershipRule(sentinel="kisuke-core"),
    EntityType.MEETING: OwnershipRule(sentinel="independent"),
    EntityType.PERSON: OwnershipRule(sentinel="independent"),
    EntityType.RESOURCE: OwnershipRule(sentinel="independent"),
    EntityType.PROJECT: OwnershipRule(owner_type=EntityType.MISSION),
    EntityType.TASK: OwnershipRule(owner_type=EntityType.PROJECT),
    EntityType.KNOWLEDGE: OwnershipRule(owner_type=EntityType.PROJECT),
    EntityType.DECISION: OwnershipRule(owner_type=EntityType.PROJECT),
    EntityType.REVIEW: OwnershipRule(owner_type=EntityType.MISSION),
    EntityType.ATTACHMENT: OwnershipRule(parent=True),
}


RELATIONSHIP_FIELDS: dict[EntityType, dict[str, frozenset[EntityType]]] = {
    EntityType.MISSION: {
        "projects": frozenset({EntityType.PROJECT}),
        "reviews": frozenset({EntityType.REVIEW}),
    },
    EntityType.PROJECT: {
        "tasks": frozenset({EntityType.TASK}),
        "knowledge": frozenset({EntityType.KNOWLEDGE}),
        "decisions": frozenset({EntityType.DECISION}),
        "meetings": frozenset({EntityType.MEETING}),
        "resources": frozenset({EntityType.RESOURCE}),
        "people": frozenset({EntityType.PERSON}),
    },
    EntityType.KNOWLEDGE: {
        "resources": frozenset({EntityType.RESOURCE}),
    },
    EntityType.MEETING: {
        "people": frozenset({EntityType.PERSON}),
        "projects": frozenset({EntityType.PROJECT}),
        "tasks": frozenset({EntityType.TASK}),
        "decisions": frozenset({EntityType.DECISION}),
        "resources": frozenset({EntityType.RESOURCE}),
    },
    EntityType.REVIEW: {
        "completed_projects": frozenset({EntityType.PROJECT}),
        "blocked_projects": frozenset({EntityType.PROJECT}),
        "next_actions": frozenset({EntityType.TASK}),
    },
}


NEXT_ACTION_OWNER: dict[EntityType, EntityType | None] = {
    EntityType.PROJECT: EntityType.TASK,
}
