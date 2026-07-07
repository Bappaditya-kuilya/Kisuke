"""Domain exceptions for Kisuke.

Recoverable validation failures are returned as structured errors. The Domain
layer raises these instead of silently continuing.
"""

from __future__ import annotations


class DomainError(Exception):
    """Base class for all domain errors."""


class ValidationError(DomainError):
    """Raised when one or more domain invariants are violated.

    Carries the list of individual problem messages.
    """

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("; ".join(self.problems))


class IdentityError(ValidationError):
    """Raised when an entity ID is malformed or duplicated."""


class OwnershipError(ValidationError):
    """Raised when an ownership rule is violated."""


class RelationshipError(ValidationError):
    """Raised when a relationship rule is violated."""


class LifecycleError(ValidationError):
    """Raised when a lifecycle/status value is invalid."""
