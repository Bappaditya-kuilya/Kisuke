from __future__ import annotations

import pytest

from kisuke.domain.exceptions import OwnershipError
from kisuke.domain.ids import EntityId
from kisuke.domain.owner import Owner


def test_kisuke_core_sentinel() -> None:
    owner = Owner.kisuke_core()
    assert owner.is_sentinel
    assert owner.sentinel == "kisuke-core"
    assert owner.entity_id is None


def test_independent_sentinel() -> None:
    owner = Owner.independent()
    assert owner.sentinel == "independent"
    assert owner.entity_id is None


def test_of_entity_id() -> None:
    eid = EntityId.generate()
    owner = Owner.of(eid)
    assert not owner.is_sentinel
    assert owner.entity_id == eid


def test_unknown_sentinel_raises() -> None:
    with pytest.raises(OwnershipError):
        Owner("unknown-sentinel")


def test_equality() -> None:
    assert Owner.kisuke_core() == Owner.kisuke_core()
    assert Owner.of(EntityId.generate()) != Owner.of(EntityId.generate())
