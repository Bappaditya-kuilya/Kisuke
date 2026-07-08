"""Validation application service.

Delegates repository validation to the Infrastructure validator and returns the
structured :class:`ValidationReport`.
"""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.validation.report import ValidationReport
from kisuke.infrastructure.validation.validator import RepositoryValidator


class ValidateService:
    """Validate the repository against the Domain Model."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def validate(self) -> ValidationReport:
        return RepositoryValidator(self.root).validate()
