"""Repository interface for the Storage layer.

Defines the contract the rest of the system uses to persist and load Domain
entities. Infrastructure implements this; the Domain never depends on it.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from kisuke.domain.entities import Entity
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import EntityType


class RepositoryError(Exception):
    """Raised when a repository operation cannot be completed."""


class EntityRepository(ABC):
    """Persists Domain entities as Markdown files, one per file."""

    @abstractmethod
    def save(self, entity: Entity) -> None:
        """Persist an entity atomically. Raises on invalid entities."""

    @abstractmethod
    def load(self, entity_type: EntityType, entity_id: EntityId) -> Entity:
        """Load an entity by type and ID."""

    @abstractmethod
    def delete(self, entity_type: EntityType, entity_id: EntityId) -> None:
        """Remove an entity if present."""

    @abstractmethod
    def exists(self, entity_type: EntityType, entity_id: EntityId) -> bool:
        """Return True if the entity file exists."""

    @abstractmethod
    def all(self, entity_type: EntityType) -> list[Entity]:
        """Return every entity of the given type, sorted by ID."""
