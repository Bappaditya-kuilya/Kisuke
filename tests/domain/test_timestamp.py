from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

import pytest

from kisuke.domain.timestamp import Timestamp


def test_now_is_utc_aware() -> None:
    ts = Timestamp.now()
    assert ts.value.tzinfo is not None
    assert ts.to_datetime().utcoffset().total_seconds() == 0


def test_from_datetime_utc() -> None:
    dt = datetime(2024, 1, 1, tzinfo=UTC)
    ts = Timestamp.from_datetime(dt)
    assert ts.to_datetime() == dt


def test_naive_datetime_raises() -> None:
    with pytest.raises(ValueError):
        Timestamp.from_datetime(datetime(2024, 1, 1))


def test_normalizes_to_utc() -> None:
    offset = timezone(timedelta(hours=5))
    ts = Timestamp.from_datetime(datetime(2024, 1, 1, 12, 0, tzinfo=offset))
    assert ts.to_datetime().utcoffset().total_seconds() == 0
    assert ts.to_datetime().hour == 7
