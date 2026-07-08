"""Validation report data structures.

A deterministic, structured representation of repository validation results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class IssueCode(StrEnum):
    """Category of a validation issue."""

    PARSE_ERROR = "PARSE_ERROR"
    SCHEMA = "SCHEMA"
    DUPLICATE_ID = "DUPLICATE_ID"
    OWNERSHIP = "OWNERSHIP"
    LIFECYCLE = "LIFECYCLE"
    ORPHAN_REFERENCE = "ORPHAN_REFERENCE"
    INVALID_REFERENCE = "INVALID_REFERENCE"


class IssueSeverity(StrEnum):
    """Severity of a validation issue."""

    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass(frozen=True)
class ValidationIssue:
    """A single, deterministic validation problem."""

    code: IssueCode
    severity: IssueSeverity
    entity_type: str | None
    entity_id: str | None
    message: str


@dataclass
class ValidationReport:
    """The complete result of validating a repository."""

    root: Path
    issues: list[ValidationIssue] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.issues.sort(key=_issue_sort_key)

    def is_valid(self) -> bool:
        return not any(i.severity == IssueSeverity.ERROR for i in self.issues)

    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == IssueSeverity.ERROR]

    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == IssueSeverity.WARNING]

    def by_code(self, code: IssueCode) -> list[ValidationIssue]:
        return [i for i in self.issues if i.code == code]

    def render_text(self) -> str:
        lines = [
            "Validation Report",
            f"Root: {self.root}",
            f"Status: {'VALID' if self.is_valid() else 'INVALID'}",
            f"Errors: {len(self.errors())}  Warnings: {len(self.warnings())}",
            "",
        ]
        for issue in self.issues:
            head = f"[{issue.severity}] {issue.code}"
            if issue.entity_type:
                head += f" {issue.entity_type}"
            if issue.entity_id:
                head += f" {issue.entity_id}"
            lines.append(f"{head}: {issue.message}")
        return "\n".join(lines) + "\n"

    def render_json(self) -> str:
        import json

        data = [
            {
                "code": i.code.value,
                "severity": i.severity.value,
                "entity_type": i.entity_type,
                "entity_id": i.entity_id,
                "message": i.message,
            }
            for i in self.issues
        ]
        return json.dumps(data, indent=2)


def _issue_sort_key(issue: ValidationIssue) -> tuple[str, str, str]:
    return (
        issue.code.value,
        issue.entity_id or "",
        issue.message,
    )
