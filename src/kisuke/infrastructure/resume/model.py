"""Resume result model.

A deterministic, Markdown-derived snapshot of the current working context.
Nothing here is inferred: every field is sourced directly from the repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from kisuke.domain.entities import (
    Decision,
    Entity,
    Knowledge,
    Meeting,
    Mission,
    Person,
    Project,
    Resource,
    Review,
    Task,
)


@dataclass
class ResumeResult:
    """The reconstructed working context for a focus Mission/Project."""

    mission: Mission | None = None
    project: Project | None = None
    next_action: Task | None = None
    related_tasks: list[Task] = field(default_factory=list)
    knowledge: list[Knowledge] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    meetings: list[Meeting] = field(default_factory=list)
    resources: list[Resource] = field(default_factory=list)
    people: list[Person] = field(default_factory=list)
    reviews: list[Review] = field(default_factory=list)

    def review_status_summary(self) -> list[str]:
        """Deterministic per-review status lines."""
        return [f"{r.review_type}: {r.status} ({r.date})" for r in self.reviews]

    def summary(self) -> str:
        lines = [
            f"Mission: {self.mission.title if self.mission else '—'}",
            f"Project: {self.project.title if self.project else '—'}",
            f"Next Action: {self.next_action.title if self.next_action else '—'}",
            f"Tasks: {len(self.related_tasks)}",
            f"Knowledge: {len(self.knowledge)}",
            f"Decisions: {len(self.decisions)}",
            f"Meetings: {len(self.meetings)}",
            f"Resources: {len(self.resources)}",
            f"People: {len(self.people)}",
            f"Reviews: {len(self.reviews)}",
        ]
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        def ident(entity: Entity) -> str:
            return str(entity.id)

        return {
            "mission": ident(self.mission) if self.mission else None,
            "project": ident(self.project) if self.project else None,
            "next_action": ident(self.next_action) if self.next_action else None,
            "related_tasks": [ident(t) for t in self.related_tasks],
            "knowledge": [ident(k) for k in self.knowledge],
            "decisions": [ident(d) for d in self.decisions],
            "meetings": [ident(m) for m in self.meetings],
            "resources": [ident(r) for r in self.resources],
            "people": [ident(p) for p in self.people],
            "reviews": [ident(r) for r in self.reviews],
        }
