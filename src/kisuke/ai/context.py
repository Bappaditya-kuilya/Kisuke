"""Context packaging.

Builds an immutable, minimal context bundle for the AI layer. AI receives only
the minimum context required, in priority order (docs/engineering/10-ai-abstraction.md):

1. Current Project
2. Current Task
3. Related Decisions
4. Relevant Knowledge
5. Resources

The packaged context is frozen: providers receive a copy and can never mutate the
canonical entities. Packaging is decoupled from any provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from kisuke.infrastructure.resume.model import ResumeResult


@dataclass(frozen=True)
class AIContext:
    """An immutable, minimal context bundle for the AI layer."""

    project: str | None
    task: str | None
    decisions: tuple[str, ...] = field(default_factory=tuple)
    knowledge: tuple[str, ...] = field(default_factory=tuple)
    resources: tuple[str, ...] = field(default_factory=tuple)
    raw: dict[str, Any] = field(default_factory=dict)

    def render(self) -> str:
        """Render the packaged context as prioritized plain text."""
        lines: list[str] = []
        if self.project:
            lines.append(f"Project:\n{self.project}")
        if self.task:
            lines.append(f"Current Task:\n{self.task}")
        if self.decisions:
            lines.append("Related Decisions:\n" + "\n".join(f"- {d}" for d in self.decisions))
        if self.knowledge:
            lines.append("Relevant Knowledge:\n" + "\n".join(f"- {k}" for k in self.knowledge))
        if self.resources:
            lines.append("Resources:\n" + "\n".join(f"- {r}" for r in self.resources))
        return "\n\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "task": self.task,
            "decisions": list(self.decisions),
            "knowledge": list(self.knowledge),
            "resources": list(self.resources),
            "raw": self.raw,
        }


def _title(entity: Any) -> str:
    title = getattr(entity, "title", None)
    return str(title) if title else ""


def _text(entity: Any) -> str:
    """Best-effort human-readable text for an entity."""
    parts: list[str] = [_title(entity)]
    for field_name in ("description", "summary", "content", "decision", "reason"):
        value = getattr(entity, field_name, "")
        if isinstance(value, str) and value:
            parts.append(value)
    return "\n".join(p for p in parts if p)


def package_context(resume: ResumeResult) -> AIContext:
    """Package a resume result into an immutable AI context bundle."""
    project_text = _text(resume.project) if resume.project is not None else None
    task_text = _text(resume.next_action) if resume.next_action is not None else None
    decisions = tuple(_text(d) for d in resume.decisions)
    knowledge = tuple(_text(k) for k in resume.knowledge)
    resources = tuple(_text(r) for r in resume.resources)

    raw = {
        "mission": _title(resume.mission) if resume.mission is not None else None,
        "project": _title(resume.project) if resume.project is not None else None,
        "next_action": _title(resume.next_action) if resume.next_action is not None else None,
        "decisions": [str(d.id) for d in resume.decisions],
        "knowledge": [str(k.id) for k in resume.knowledge],
        "resources": [str(r.id) for r in resume.resources],
        "related_tasks": [str(t.id) for t in resume.related_tasks],
    }

    return AIContext(
        project=project_text,
        task=task_text,
        decisions=decisions,
        knowledge=knowledge,
        resources=resources,
        raw=raw,
    )
