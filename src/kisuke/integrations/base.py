"""Integration base class.

A small, optional base for concrete integrations. Integrations are adapters:
they may read, import, export, synchronize, and open, but they never own Kisuke
data and never modify the core architecture.
"""

from __future__ import annotations

from typing import Any

from kisuke.plugins.interfaces import Integration


class BaseIntegration(Integration):
    """Convenience base implementing option storage."""

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        self._options: dict[str, Any] = dict(options or {})

    def configure(self, options: dict[str, Any]) -> None:
        self._options.update(options)

    def option(self, key: str, default: Any = None) -> Any:
        return self._options.get(key, default)
