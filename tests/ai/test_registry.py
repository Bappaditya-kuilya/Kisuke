"""Tests for the provider registry (provider selection)."""

from __future__ import annotations

from kisuke.ai.registry import ProviderRegistry
from tests.ai.conftest import MockProvider


def test_register_and_get() -> None:
    reg = ProviderRegistry()
    reg.register(MockProvider())
    assert reg.get("mock") is not None
    assert reg.get("missing") is None


def test_register_requires_name() -> None:
    reg = ProviderRegistry()
    bad = MockProvider()
    bad.name = ""
    with __import__("pytest").raises(ValueError):
        reg.register(bad)


def test_available_filters_unavailable() -> None:
    reg = ProviderRegistry()
    reg.register(MockProvider(available=False))
    reg.register(MockProvider(available=True))
    available = reg.available()
    assert len(available) == 1
    assert available[0].name == "mock"


def test_select_by_name() -> None:
    reg = ProviderRegistry()
    reg.register(MockProvider(available=True))
    assert reg.select("mock") is not None
    assert reg.select("unknown") is None


def test_select_falls_back_to_first_available() -> None:
    reg = ProviderRegistry()
    reg.register(MockProvider(available=False, ))
    reg.register(MockProvider(available=True))
    # Requesting the unavailable one falls back to the available provider.
    chosen = reg.select("mock")
    assert chosen is not None
    assert chosen.is_available() is True


def test_select_returns_none_when_empty() -> None:
    reg = ProviderRegistry()
    assert reg.select() is None
