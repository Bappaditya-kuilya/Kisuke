"""Domain validation.

Enforces the Domain Model invariants: identity uniqueness, ownership rules,
relationship validity, and lifecycle validity. Validation is pure: it takes
entities in memory and raises structured :class:`ValidationError` on violation.
"""

from __future__ import annotations

from enum import StrEnum
from typing import cast

from .entities import Entity
from .exceptions import (
    IdentityError,
    LifecycleError,
    OwnershipError,
    RelationshipError,
)
from .ids import EntityId
from .lifecycle import STATUS_ENUMS, EntityType
from .relationships import NEXT_ACTION_OWNER, OWNERSHIP_RULES, RELATIONSHIP_FIELDS


def validate_status(entity_type: EntityType, status: StrEnum) -> None:
    """Raise LifecycleError if ``status`` is not valid for ``entity_type``."""
    allowed = STATUS_ENUMS.get(entity_type)
    if allowed is None or not isinstance(status, allowed):
        raise LifecycleError([f"{entity_type} has no status {status!r}"])


def validate_entity(entity: Entity) -> None:
    """Validate a single entity's structural invariants (no collection needed)."""
    lifecycle = _check_lifecycle(entity)
    ownership = _check_ownership_structure(entity)
    if ownership:
        raise OwnershipError(ownership)
    if lifecycle:
        raise LifecycleError(lifecycle)


def validate_entities(entities: list[Entity]) -> None:
    """Validate a collection of entities against all Domain Model invariants."""
    identity: list[str] = []
    ownership: list[str] = []
    lifecycle: list[str] = []
    relationship: list[str] = []
    by_id: dict[EntityId, Entity] = {}

    for entity in entities:
        if entity.id in by_id:
            identity.append(f"Duplicate entity ID: {entity.id}")
        else:
            by_id[entity.id] = entity

    for entity in entities:
        lifecycle += _check_lifecycle(entity)
        ownership += _check_ownership_structure(entity)

    for entity in entities:
        ownership += _check_ownership_target(entity, by_id)
        relationship += _check_relationships(entity, by_id)

    if identity:
        raise IdentityError(identity)
    if ownership:
        raise OwnershipError(ownership)
    if relationship:
        raise RelationshipError(relationship)
    if lifecycle:
        raise LifecycleError(lifecycle)


def _check_lifecycle(entity: Entity) -> list[str]:
    problems: list[str] = []
    try:
        validate_status(entity.entity_type, cast(StrEnum, entity.status))
    except LifecycleError as exc:
        problems += exc.problems
    return problems


def _check_ownership_structure(entity: Entity) -> list[str]:
    problems: list[str] = []
    rule = OWNERSHIP_RULES[entity.entity_type]
    if rule.sentinel is not None:
        if entity.owner.sentinel != rule.sentinel:
            problems.append(
                f"{entity.entity_type} must be owned by sentinel "
                f"{rule.sentinel!r}, got {entity.owner!r}"
            )
    elif rule.owner_type is not None or rule.parent:
        if entity.owner.entity_id is None:
            problems.append(
                f"{entity.entity_type} {entity.id} must be owned by an entity, "
                f"got sentinel {entity.owner.sentinel!r}"
            )
    return problems


def _check_ownership_target(entity: Entity, by_id: dict[EntityId, Entity]) -> list[str]:
    problems: list[str] = []
    rule = OWNERSHIP_RULES[entity.entity_type]
    owner_id = entity.owner.entity_id
    if owner_id is None:
        return problems
    owner_entity = by_id.get(owner_id)
    if owner_entity is None:
        problems.append(f"{entity.entity_type} {entity.id} references missing owner {owner_id}")
    elif rule.owner_type is not None and owner_entity.entity_type != rule.owner_type:
        problems.append(
            f"{entity.entity_type} {entity.id} owned by {owner_entity.entity_type} "
            f"but expected {rule.owner_type}"
        )
    return problems


def _check_relationships(entity: Entity, by_id: dict[EntityId, Entity]) -> list[str]:
    problems: list[str] = []

    typed_fields = RELATIONSHIP_FIELDS.get(entity.entity_type, {})
    for field_name, allowed in typed_fields.items():
        seen: set[EntityId] = set()
        for ref in getattr(entity, field_name):
            problems += _check_one_reference(entity, ref, allowed, seen, by_id)

    seen = set()
    for ref in entity.references:
        problems += _check_one_reference(entity, ref, None, seen, by_id)

    seen = set()
    for ref in entity.attachments:
        problems += _check_one_reference(
            entity, ref, frozenset({EntityType.ATTACHMENT}), seen, by_id
        )

    next_type = NEXT_ACTION_OWNER.get(entity.entity_type)
    if next_type is not None:
        next_action = getattr(entity, "next_action", None)
        if next_action is not None:
            problems += _check_one_reference(
                entity, next_action, frozenset({next_type}), set(), by_id
            )

    return problems


def _check_one_reference(
    entity: Entity,
    ref: EntityId,
    allowed: frozenset[EntityType] | None,
    seen: set[EntityId],
    by_id: dict[EntityId, Entity],
) -> list[str]:
    problems: list[str] = []
    if ref in seen:
        problems.append(f"Duplicate reference {ref} in {entity.entity_type} {entity.id}")
        return problems
    seen.add(ref)

    target = by_id.get(ref)
    if target is None:
        problems.append(f"{entity.entity_type} {entity.id} references missing entity {ref}")
        return problems
    if allowed is not None and target.entity_type not in allowed:
        problems.append(
            f"{entity.entity_type} {entity.id} references disallowed type "
            f"{target.entity_type} via {ref}"
        )
    return problems
