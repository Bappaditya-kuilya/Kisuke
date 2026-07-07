"""Owner value object.

Every entity has exactly one owner. The owner is either a reserved sentinel
(``kisuke-core`` or ``independent``) or the ID of a specific domain entity
instance. Reserved sentinels are terminal owner values and never resolve to an
entity record.
"""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import OwnershipError
from .ids import EntityId

KNOWN_SENTINELS = ("kisuke-core", "independent")


@dataclass(frozen=True)
class Owner:
    """The single owner of an entity."""

    value: str | EntityId

    @classmethod
    def kisuke_core(cls) -> Owner:
        return cls("kisuke-core")

    @classmethod
    def independent(cls) -> Owner:
        return cls("independent")

    @classmethod
    def of(cls, entity_id: EntityId) -> Owner:
        return cls(entity_id)

    @property
    def is_sentinel(self) -> bool:
        return isinstance(self.value, str)

    @property
    def sentinel(self) -> str | None:
        return self.value if isinstance(self.value, str) else None

    @property
    def entity_id(self) -> EntityId | None:
        return self.value if isinstance(self.value, EntityId) else None

    def __post_init__(self) -> None:
        if isinstance(self.value, str) and self.value not in KNOWN_SENTINELS:
            raise OwnershipError([f"Unknown owner sentinel: {self.value!r}"])
