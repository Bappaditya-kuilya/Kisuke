"""Tests for integration configuration.

The :class:`IntegrationConfig` facade reads and writes enable/disable state and
per-integration options through the plugin registry, without touching canonical
data. Disabling an integration never affects core functionality.
"""

from __future__ import annotations

from kisuke.integrations import IntegrationConfig


def test_config_enable_disable(registry: object) -> None:
    from kisuke.plugins.registry import PluginRegistry

    assert isinstance(registry, PluginRegistry)
    config = IntegrationConfig(registry)
    assert config.is_enabled("git") is False
    config.set_enabled("git", True)
    assert config.is_enabled("git") is True
    config.set_option("git", "author", "me")
    assert config.get_option("git", "author") == "me"
    config.set_enabled("git", False)
    assert config.is_enabled("git") is False


def test_config_describe(registry: object) -> None:
    from kisuke.plugins.registry import PluginRegistry

    assert isinstance(registry, PluginRegistry)
    config = IntegrationConfig(registry)
    entries = config.describe()
    names = {entry.info.name for entry in entries}
    assert "git" in names
    git_entry = next(e for e in entries if e.info.name == "git")
    assert git_entry.info.category == "development"
