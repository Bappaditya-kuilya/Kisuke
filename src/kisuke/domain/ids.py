"""Entity identifiers.

Entity IDs are immutable value objects wrapping a UUID. IDs are globally unique
and never change once assigned.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from .exceptions import IdentityError

_ID_FACTORY = uuid.uuid4


@dataclass(frozen=True)
class EntityId:
    """Globally unique, immutable identifier for any Kisuke entity."""

    value: uuid.UUID

    @classmethod
    def generate(cls) -> EntityId:
        return cls(_ID_FACTORY())

    @classmethod
    def from_uuid(cls, value: uuid.UUID) -> EntityId:
        return cls(value)

    @classmethod
    def from_string(cls, value: str) -> EntityId:
        try:
            return cls(uuid.UUID(value))
        except (ValueError, AttributeError, TypeError) as exc:
            raise IdentityError([f"Invalid EntityId: {value!r}"]) from exc

    def __str__(self) -> str:
        return str(self.value)
