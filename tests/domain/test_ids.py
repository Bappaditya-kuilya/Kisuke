from __future__ import annotations

import uuid

import pytest

from kisuke.domain.exceptions import IdentityError
from kisuke.domain.ids import EntityId


def test_generate_returns_unique_id() -> None:
    a = EntityId.generate()
    b = EntityId.generate()
    assert isinstance(a.value, uuid.UUID)
    assert a != b


def test_from_uuid_roundtrip() -> None:
    u = uuid.uuid4()
    eid = EntityId.from_uuid(u)
    assert eid.value == u
    assert EntityId.from_uuid(u) == eid


def test_from_string_roundtrip() -> None:
    s = "00000000-0000-0000-0000-000000000001"
    eid = EntityId.from_string(s)
    assert str(eid) == s


@pytest.mark.parametrize("bad", ["not-a-uuid", "", "00000000-0000-0000-0000"])
def test_from_string_invalid_raises(bad: str) -> None:
    with pytest.raises(IdentityError):
        EntityId.from_string(bad)


def test_equality_and_hash() -> None:
    s = "00000000-0000-0000-0000-000000000001"
    assert EntityId.from_string(s) == EntityId.from_string(s)
    assert hash(EntityId.from_string(s)) == hash(EntityId.from_string(s))
