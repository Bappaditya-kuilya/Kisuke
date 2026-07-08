"""Resume application service.

Wraps the :class:`ResumeService`, optionally using the search index, and
persists the last requested focus so ``resume --last`` is reproducible.
"""

from __future__ import annotations

import json
from pathlib import Path

from kisuke.infrastructure.resume.model import ResumeResult
from kisuke.infrastructure.resume.service import ResumeService
from kisuke.infrastructure.search.api import SearchEngine


class ResumeApp:
    """Reconstruct the working context for a focus Mission/Project."""

    def __init__(
        self, root: Path, db_path: Path | None = None, last_focus_path: Path | None = None
    ) -> None:
        self.root = Path(root)
        self.db_path = Path(db_path) if db_path is not None else None
        self.last_focus_path = Path(last_focus_path) if last_focus_path is not None else None

    def _load_last(self) -> dict[str, str | None]:
        if self.last_focus_path is None or not self.last_focus_path.exists():
            return {}
        try:
            data = json.loads(self.last_focus_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
        if not isinstance(data, dict):
            return {}
        return {k: data.get(k) for k in ("mission", "project")}

    def _save_last(self, mission: str | None, project: str | None) -> None:
        if self.last_focus_path is None:
            return
        self.last_focus_path.parent.mkdir(parents=True, exist_ok=True)
        self.last_focus_path.write_text(
            json.dumps({"mission": mission, "project": project}, indent=2), encoding="utf-8"
        )

    def resume(
        self,
        mission: str | None = None,
        project: str | None = None,
        last: bool = False,
    ) -> ResumeResult:
        focus_mission: str | None = None
        focus_project: str | None = None
        if last:
            saved = self._load_last()
            focus_mission = saved.get("mission")
            focus_project = saved.get("project")
        else:
            focus_mission = mission
            focus_project = project
            if mission is not None or project is not None:
                self._save_last(mission, project)

        search: SearchEngine | None = None
        if self.db_path is not None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            search = SearchEngine(self.db_path)
        try:
            return ResumeService(self.root, search).resume(focus_mission, focus_project)
        finally:
            if search is not None:
                search.close()
