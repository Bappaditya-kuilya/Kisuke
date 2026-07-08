"""Infrastructure storage package.

Pure Infrastructure layer: persists Domain entities as Markdown. Depends on the
Domain for entity definitions and validation only; contains no business rules.
"""

from __future__ import annotations

from .interfaces import EntityRepository, RepositoryError
from .repository import FileRepository
from .serializer import entity_to_markdown, markdown_to_entity

__all__ = [
    "EntityRepository",
    "FileRepository",
    "RepositoryError",
    "entity_to_markdown",
    "markdown_to_entity",
]
