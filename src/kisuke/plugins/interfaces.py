"""Plugin and integration interfaces.

Defines the contracts every Kisuke integration (Git, GitHub, Obsidian, Calendar,
AI, …) implements. Integrations are adapters only: they may read, import,
export, synchronize, and open external resources, but they never own Kisuke
data and never modify the core architecture. All integrations are optional and
pluggable; the core functions without any of them.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IntegrationInfo:
    """Static, machine-readable description of an integration."""

    name: str
    category: str
    description: str
    available: bool


class Integration(ABC):
    """Base contract for an optional, pluggable integration adapter."""

    name: str = ""
    category: str = "generic"
    description: str = ""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the integration can operate in this environment."""

    def configure(self, options: dict[str, Any]) -> None:  # noqa: B027
        """Apply integration-specific options.

        Integrations with no options may rely on this default no-op, while
        the :class:`~kisuke.integrations.base.BaseIntegration` subclass adds
        option storage. Only ``is_available`` is mandatory.
        """
        pass

    def info(self) -> IntegrationInfo:
        """Return a static description of this integration."""
        return IntegrationInfo(self.name, self.category, self.description, self.is_available())
