"""Review application service.

The CLI exposes review commands (morning / weekly / monthly / quarterly). These
produce a deterministic, read-only aggregation of the current repository using
the Resume engine and stored Review entities. The persistent review engine is a
later milestone; this service reports working context without mutating data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kisuke.domain.entities import Review
from kisuke.domain.lifecycle import EntityType
from kisuke.domain.timestamp import Timestamp
from kisuke.infrastructure.resume.model import ResumeResult
from kisuke.infrastructure.resume.service import ResumeService
from kisuke.infrastructure.search.api import SearchEngine
from kisuke.infrastructure.storage.repository import FileRepository


@dataclass
class ReviewReport:
    """A rendered review: human markdown plus machine-readable data."""

    kind: str
    generated_at: str
    markdown: str
    data: dict[str, Any] = field(default_factory=dict)


class ReviewService:
    """Aggregate working context into review reports."""

    def __init__(self, root: Path, db_path: Path | None = None) -> None:
        self.root = Path(root)
        self.db_path = Path(db_path) if db_path is not None else None

    def _search(self) -> SearchEngine | None:
        if self.db_path is None:
            return None
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return SearchEngine(self.db_path)

    def _resume(self, search: SearchEngine | None) -> ResumeResult:
        return ResumeService(self.root, search).resume()

    def morning(self) -> ReviewReport:
        search = self._search()
        try:
            result = self._resume(search)
        finally:
            if search is not None:
                search.close()
        generated = Timestamp.now().to_datetime().isoformat()
        lines = ["# Morning Review", "", f"Generated: {generated}", ""]
        lines.append(f"Mission: {result.mission.title if result.mission else '—'}")
        lines.append(f"Project: {result.project.title if result.project else '—'}")
        lines.append(f"Next Action: {result.next_action.title if result.next_action else '—'}")
        lines.append("")
        lines.append(f"Tasks: {len(result.related_tasks)}")
        lines.append(f"Knowledge: {len(result.knowledge)}")
        lines.append(f"Decisions: {len(result.decisions)}")
        lines.append(f"Meetings: {len(result.meetings)}")
        lines.append(f"Resources: {len(result.resources)}")
        lines.append(f"People: {len(result.people)}")
        lines.append(f"Reviews: {len(result.reviews)}")
        markdown = "\n".join(lines) + "\n"
        data: dict[str, object] = {
            "kind": "morning",
            "generated_at": generated,
            "mission": str(result.mission.id) if result.mission else None,
            "project": str(result.project.id) if result.project else None,
            "next_action": str(result.next_action.id) if result.next_action else None,
            "counts": {
                "tasks": len(result.related_tasks),
                "knowledge": len(result.knowledge),
                "decisions": len(result.decisions),
                "meetings": len(result.meetings),
                "resources": len(result.resources),
                "people": len(result.people),
                "reviews": len(result.reviews),
            },
        }
        return ReviewReport("morning", generated, markdown, data)

    def period(self, kind: str) -> ReviewReport:
        search = self._search()
        try:
            result = self._resume(search)
        finally:
            if search is not None:
                search.close()
        generated = Timestamp.now().to_datetime().isoformat()
        repo = FileRepository(self.root)
        matching: list[Review] = [
            r
            for r in repo.all(EntityType.REVIEW)
            if isinstance(r, Review) and r.review_type.lower() == kind.lower()
        ]
        lines = ["# " + kind.title() + " Review", "", f"Generated: {generated}", ""]
        lines.append(f"Mission: {result.mission.title if result.mission else '—'}")
        lines.append(f"Project: {result.project.title if result.project else '—'}")
        lines.append(f"Next Action: {result.next_action.title if result.next_action else '—'}")
        lines.append("")
        lines.append(f"Existing {kind.title()} Reviews:")
        if matching:
            for review in matching:
                lines.append(
                    f"- {review.title} ({review.id}) status={review.status} date={review.date}"
                )
        else:
            lines.append("  none")
        lines.append("")
        lines.append("Context:")
        lines.append(f"  Decisions: {len(result.decisions)}")
        lines.append(f"  Meetings: {len(result.meetings)}")
        lines.append(f"  Projects: {len([1]) if result.project else 0}")
        markdown = "\n".join(lines) + "\n"
        data = {
            "kind": kind,
            "generated_at": generated,
            "mission": str(result.mission.id) if result.mission else None,
            "project": str(result.project.id) if result.project else None,
            "next_action": str(result.next_action.id) if result.next_action else None,
            "reviews": [str(r.id) for r in matching],
            "context": {
                "decisions": len(result.decisions),
                "meetings": len(result.meetings),
            },
        }
        return ReviewReport(kind, generated, markdown, data)
