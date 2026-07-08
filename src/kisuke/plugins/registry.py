"""Plugin registry.

Discovers and tracks integrations. Built-in integrations are registered
explicitly; external plugins can be dropped into a plugins directory and are
loaded through their public ``register`` hook. Enabled/disabled state and
per-integration options are persisted as JSON so the configuration survives
restarts. Only the registry persists state; it never touches canonical data.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

from kisuke.plugins.interfaces import Integration, IntegrationInfo


class PluginRegistry:
    """Registry of available and enabled integrations."""

    def __init__(self, config_path: Path) -> None:
        self.config_path = Path(config_path)
        self._integrations: dict[str, Integration] = {}
        self._state = self._load()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register(self, integration: Integration) -> None:
        if not integration.name:
            raise ValueError("integration must declare a non-empty name")
        self._integrations[integration.name] = integration
        enabled = self._state.setdefault("enabled", {})
        enabled[integration.name] = enabled.get(integration.name, False)

    def discover(self, plugins_dir: Path | None = None) -> list[Integration]:
        """Return all registered integrations (built-in + discovered)."""
        if plugins_dir is not None:
            self._discover_directory(Path(plugins_dir))
        return list(self._integrations.values())

    def _discover_directory(self, plugins_dir: Path) -> None:
        if not plugins_dir.is_dir():
            return
        for path in sorted(plugins_dir.glob("*.py")):
            if path.name == "__init__.py":
                continue
            self._load_plugin_module(path)

    def _load_plugin_module(self, path: Path) -> None:
        try:
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if spec is None or spec.loader is None:
                return
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # noqa: S604 - local plugin only
            register_fn = getattr(module, "register", None)
            if callable(register_fn):
                register_fn(self)
        except Exception:  # noqa: BLE001 - never let a bad plugin break core
            return

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def list_integrations(self) -> list[IntegrationInfo]:
        return [integration.info() for integration in self._integrations.values()]

    def get(self, name: str) -> Integration | None:
        return self._integrations.get(name)

    def is_enabled(self, name: str) -> bool:
        return bool(self._state.get("enabled", {}).get(name, False))

    def enabled(self) -> list[Integration]:
        return [
            integration
            for integration in self._integrations.values()
            if self.is_enabled(integration.name) and integration.is_available()
        ]

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def enable(self, name: str) -> None:
        if not self._is_known(name):
            raise KeyError(f"unknown integration: {name}")
        self._state.setdefault("enabled", {})[name] = True
        self._save()

    def disable(self, name: str) -> None:
        if not self._is_known(name):
            raise KeyError(f"unknown integration: {name}")
        self._state.setdefault("enabled", {})[name] = False
        self._save()

    def set_option(self, name: str, key: str, value: Any) -> None:
        if not self._is_known(name):
            raise KeyError(f"unknown integration: {name}")
        options = self._state.setdefault("options", {}).setdefault(name, {})
        options[key] = value
        self._save()

    def _is_known(self, name: str) -> bool:
        if name in self._integrations:
            return True
        state = self._state
        return name in state.get("enabled", {}) or name in state.get("options", {})

    def get_option(self, name: str, key: str, default: Any = None) -> Any:
        return self._state.get("options", {}).get(name, {}).get(key, default)

    def get_options(self, name: str) -> dict[str, Any]:
        return dict(self._state.get("options", {}).get(name, {}))

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {}
        try:
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
        return data if isinstance(data, dict) else {}

    def _save(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self._state, indent=2), encoding="utf-8")
