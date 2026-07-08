"""Integration configuration.

A configuration-centric facade over the :class:`PluginRegistry`. It exposes
per-integration enable/disable state and options without touching canonical
data. Configuration is persisted as JSON by the registry. Integrations are
optional: disabling one never affects core functionality.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from kisuke.plugins.interfaces import IntegrationInfo
from kisuke.plugins.registry import PluginRegistry


@dataclass
class IntegrationConfigEntry:
    """Combined description + configuration for one integration."""

    info: IntegrationInfo
    enabled: bool
    options: dict[str, Any] = field(default_factory=dict)


class IntegrationConfig:
    """Read/write integration configuration through the registry."""

    def __init__(self, registry: PluginRegistry) -> None:
        self.registry = registry

    def set_enabled(self, name: str, enabled: bool) -> None:
        if enabled:
            self.registry.enable(name)
        else:
            self.registry.disable(name)

    def is_enabled(self, name: str) -> bool:
        return self.registry.is_enabled(name)

    def set_option(self, name: str, key: str, value: Any) -> None:
        self.registry.set_option(name, key, value)

    def get_option(self, name: str, key: str, default: Any = None) -> Any:
        return self.registry.get_option(name, key, default)

    def describe(self) -> list[IntegrationConfigEntry]:
        entries: list[IntegrationConfigEntry] = []
        for info in self.registry.list_integrations():
            entries.append(
                IntegrationConfigEntry(
                    info=info,
                    enabled=self.registry.is_enabled(info.name),
                    options=self.registry.get_options(info.name),
                )
            )
        return entries
