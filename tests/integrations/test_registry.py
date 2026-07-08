"""Tests for the plugin interface and registry."""

from __future__ import annotations

from pathlib import Path

import pytest

from kisuke.plugins.interfaces import Integration
from kisuke.plugins.registry import PluginRegistry


class _FakeIntegration(Integration):
    name = "fake"
    category = "test"
    description = "A fake integration for tests."

    def __init__(self) -> None:
        self.configured: dict = {}

    def is_available(self) -> bool:
        return True

    def configure(self, options: dict) -> None:  # type: ignore[override]
        self.configured.update(options)


def test_registry_register_and_list(tmp_path: Path) -> None:
    reg = PluginRegistry(tmp_path / "integrations.json")
    reg.register(_FakeIntegration())
    info = reg.list_integrations()
    assert len(info) == 1
    assert info[0].name == "fake"
    assert info[0].available is True


def test_registry_enable_disable_persists(tmp_path: Path) -> None:
    path = tmp_path / "integrations.json"
    reg = PluginRegistry(path)
    reg.register(_FakeIntegration())
    reg.enable("fake")
    assert reg.is_enabled("fake") is True

    reg2 = PluginRegistry(path)
    assert reg2.is_enabled("fake") is True
    reg2.disable("fake")
    assert reg2.is_enabled("fake") is False


def test_registry_options(tmp_path: Path) -> None:
    reg = PluginRegistry(tmp_path / "integrations.json")
    reg.register(_FakeIntegration())
    reg.set_option("fake", "token", "abc")
    assert reg.get_option("fake", "token") == "abc"
    assert reg.get_options("fake") == {"token": "abc"}


def test_registry_get_and_unknown(tmp_path: Path) -> None:
    reg = PluginRegistry(tmp_path / "integrations.json")
    reg.register(_FakeIntegration())
    assert reg.get("fake") is not None
    assert reg.get("missing") is None
    with pytest.raises(KeyError):
        reg.enable("missing")


def test_registry_discovers_plugins(tmp_path: Path) -> None:
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    module = plugins_dir / "myplugin.py"
    module.write_text(
        "from kisuke.plugins.interfaces import Integration\n"
        "class MyPlugin(Integration):\n"
        "    name = 'mine'\n"
        "    category = 'test'\n"
        "    description = 'external'\n"
        "    def is_available(self): return True\n"
        "def register(registry):\n"
        "    registry.register(MyPlugin())\n",
        encoding="utf-8",
    )
    reg = PluginRegistry(tmp_path / "integrations.json")
    reg.register(_FakeIntegration())
    reg.discover(plugins_dir)
    assert reg.get("mine") is not None
    assert {i.name for i in reg.list_integrations()} == {"fake", "mine"}


def test_registry_bad_plugin_is_ignored(tmp_path: Path) -> None:
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "broken.py").write_text("raise ValueError('boom')\n", encoding="utf-8")
    reg = PluginRegistry(tmp_path / "integrations.json")
    reg.register(_FakeIntegration())
    reg.discover(plugins_dir)  # must not raise
    assert reg.get("fake") is not None
