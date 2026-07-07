"""Timestamp value object.

Timestamps are stored in UTC. This value object normalizes any timezone-aware
datetime to UTC and rejects naive datetimes, keeping the Domain layer explicit
about time handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Timestamp:
    """An immutable UTC timestamp."""

    value: datetime

    def __post_init__(self) -> None:
        if self.value.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware (UTC)")
        object.__setattr__(self, "value", self.value.astimezone(UTC))

    @classmethod
    def now(cls) -> Timestamp:
        return cls(datetime.now(UTC))

    @classmethod
    def from_datetime(cls, value: datetime) -> Timestamp:
        return cls(value)

    def to_datetime(self) -> datetime:
        return self.value
