"""Configuration application service.

Configuration is external: environment variables take precedence, and a settings
file (JSON) stores user overrides. This service reads, writes, and opens that
settings file. It never hardcodes secrets.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from kisuke.shared.config import CACHE_DIR_NAME, INDEX_DIR_NAME, Config

VALID_KEYS = ("repo_dir", "data_dir", "log_level")


def default_settings_path() -> Path:
    from kisuke.application.workspace import default_settings_path

    return default_settings_path()


def resolve_config() -> Config:
    """Build a :class:`Config` merging environment and settings overrides."""
    base = Config.from_env()
    settings = ConfigService(default_settings_path()).load()
    data_dir_value = settings.get("data_dir")
    data_dir = Path(str(data_dir_value)) if data_dir_value else base.data_dir
    return Config(
        data_dir=data_dir,
        index_dir=data_dir / INDEX_DIR_NAME,
        cache_dir=data_dir / CACHE_DIR_NAME,
        log_level=base.log_level,
    )


class ConfigService:
    """Read and write the user settings file."""

    def __init__(self, settings_path: Path) -> None:
        self.settings_path = Path(settings_path)

    def load(self) -> dict[str, object]:
        if not self.settings_path.exists():
            return {}
        try:
            data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, data: dict[str, object]) -> None:
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get(self, key: str | None = None) -> dict[str, object]:
        settings = self.load()
        view: dict[str, object] = {
            "repo_dir": settings.get("repo_dir"),
            "data_dir": settings.get("data_dir"),
            "log_level": settings.get("log_level"),
        }
        if key is None:
            return view
        return {key: view.get(key)}

    def set(self, key: str, value: str) -> dict[str, object]:
        if key not in VALID_KEYS:
            raise ValueError(f"unknown config key: {key} (expected one of {', '.join(VALID_KEYS)})")
        data = self.load()
        data[key] = value
        self.save(data)
        return {key: value}

    def edit(self) -> Path:
        editor = os.environ.get("EDITOR", "vi")
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.settings_path.exists():
            self.settings_path.write_text("{}\n", encoding="utf-8")
        subprocess.run([editor, str(self.settings_path)], check=False)  # noqa: S603
        return self.settings_path
