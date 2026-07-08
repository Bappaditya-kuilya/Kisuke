"""Plugin application service.

Plugins are isolated (M10). The CLI exposes a minimal registry so the plugin
commands are functional and deterministic offline: a JSON file listing
registered plugins. Installation records metadata; removal and update operate on
that record. No plugin code is executed here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Plugin:
    """A registered plugin record."""

    name: str
    source: str | None


class PluginService:
    """Manage the local plugin registry."""

    def __init__(self, registry_path: Path) -> None:
        self.registry_path = Path(registry_path)

    def _read(self) -> list[dict[str, object]]:
        if not self.registry_path.exists():
            return []
        try:
            data = json.loads(self.registry_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return []
        return data if isinstance(data, list) else []

    def _write(self, items: list[dict[str, object]]) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(json.dumps(items, indent=2), encoding="utf-8")

    def list_plugins(self) -> list[Plugin]:
        return [Plugin(str(i.get("name", "")), _as_source(i.get("source"))) for i in self._read()]

    def install(self, name: str, source: str | None = None) -> Plugin:
        items = self._read()
        if any(str(i.get("name")) == name for i in items):
            raise ValueError(f"plugin already installed: {name}")
        items.append({"name": name, "source": source})
        self._write(items)
        return Plugin(name, source)

    def remove(self, name: str) -> bool:
        items = self._read()
        kept = [i for i in items if str(i.get("name")) != name]
        if len(kept) == len(items):
            return False
        self._write(kept)
        return True

    def update(self, name: str | None = None) -> list[Plugin]:
        items = self._read()
        if name is not None and not any(str(i.get("name")) == name for i in items):
            raise ValueError(f"plugin not installed: {name}")
        return [Plugin(str(i.get("name", "")), _as_source(i.get("source"))) for i in items]


def _as_source(value: object) -> str | None:
    return str(value) if value is not None else None
