"""Configuration for Kisuke.

Settings are resolved from environment variables with safe defaults. Paths and
secrets are never hardcoded; secrets are read from the environment only.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / ".local" / "share" / "kisuke"
INDEX_DIR_NAME = "index"
CACHE_DIR_NAME = "cache"


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else default


def _log_level_from_env() -> int:
    raw = os.environ.get("KISUKE_LOG_LEVEL", "INFO").upper()
    return getattr(logging, raw, logging.INFO)


@dataclass(frozen=True)
class Config:
    data_dir: Path
    index_dir: Path
    cache_dir: Path
    log_level: int

    def ensure_dirs(self) -> None:
        """Create data, index, and cache directories if missing."""
        for directory in (self.data_dir, self.index_dir, self.cache_dir):
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls) -> Config:
        data_dir = _env_path("KISUKE_DATA_DIR", DEFAULT_DATA_DIR)
        return cls(
            data_dir=data_dir,
            index_dir=data_dir / INDEX_DIR_NAME,
            cache_dir=data_dir / CACHE_DIR_NAME,
            log_level=_log_level_from_env(),
        )
