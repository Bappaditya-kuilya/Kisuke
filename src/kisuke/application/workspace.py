"""Repository workspace resolution and initialization.

The CLI operates on a Markdown repository rooted at a directory. The root is
resolved from ``KISUKE_REPO_DIR`` (or a configured ``repo_dir``) and otherwise
defaults to the current working directory. ``init`` creates the canonical
type-specific folders defined by the Storage layer.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from kisuke.infrastructure.storage.repository import FOLDER_NAMES


def default_settings_path() -> Path:
    """Path to the user settings file inside the resolved data directory."""
    from kisuke.shared.config import Config

    return Config.from_env().data_dir / "settings.json"


def _load_settings_file(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def resolve_repo_root() -> Path:
    """Resolve the repository root from environment, settings, or cwd."""
    env = os.environ.get("KISUKE_REPO_DIR")
    if env:
        return Path(env).expanduser()
    settings = _load_settings_file(default_settings_path())
    repo_dir = settings.get("repo_dir")
    if isinstance(repo_dir, str) and repo_dir.strip():
        return Path(repo_dir).expanduser()
    return Path.cwd()


def init_repository(root: Path) -> list[str]:
    """Create the canonical entity folders under ``root``.

    Returns the list of folders that were created (omits existing ones).
    """
    root = Path(root)
    created: list[str] = []
    for folder in FOLDER_NAMES.values():
        directory = root / folder
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(str(directory))
    return created


def repository_status(root: Path) -> dict[str, object]:
    """Return a deterministic status summary for the repository."""
    root = Path(root)
    counts: dict[str, int] = {}
    for et, folder in FOLDER_NAMES.items():
        directory = root / folder
        counts[et.value] = len(list(directory.glob("*.md"))) if directory.is_dir() else 0
    return {
        "root": str(root),
        "initialized": root.is_dir(),
        "counts": counts,
    }
