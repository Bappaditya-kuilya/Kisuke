"""Schema validation for raw entity frontmatter.

Checks the Universal Entity Schema invariants on the parsed frontmatter mapping
*before* entity construction, producing friendly ``SCHEMA`` issues. This catches
malformed files (missing required fields, wrong shapes) without relying on
construction exceptions.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.validation.report import (
    IssueCode,
    IssueSeverity,
    ValidationIssue,
)

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

REQUIRED_FIELDS = ("id", "type", "title", "owner", "status", "created_at", "updated_at")
LIST_FIELDS = ("tags", "references", "attachments")


def safe_entity_type(value: Any) -> EntityType | None:
    if not isinstance(value, str):
        return None
    try:
        return EntityType(value)
    except ValueError:
        return None


def safe_entity_id(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if UUID_RE.match(value):
        return value
    return None


def schema_issues(fm: dict[str, Any], entity_type: EntityType | None) -> list[ValidationIssue]:
    """Return SCHEMA issues for the given frontmatter mapping."""
    issues: list[ValidationIssue] = []
    entity_id = safe_entity_id(fm.get("id"))

    for field_name in REQUIRED_FIELDS:
        if field_name not in fm or fm[field_name] is None:
            issues.append(
                ValidationIssue(
                    IssueCode.SCHEMA,
                    IssueSeverity.ERROR,
                    entity_type,
                    entity_id,
                    f"Missing required field '{field_name}'",
                )
            )

    raw_id = fm.get("id")
    if raw_id is not None and not (isinstance(raw_id, str) and UUID_RE.match(raw_id)):
        issues.append(
            ValidationIssue(
                IssueCode.SCHEMA,
                IssueSeverity.ERROR,
                entity_type,
                entity_id,
                f"Field 'id' is not a valid UUID: {raw_id!r}",
            )
        )

    for field_name in ("owner", "status"):
        value = fm.get(field_name)
        if value is not None and not str(value).strip():
            issues.append(
                ValidationIssue(
                    IssueCode.SCHEMA,
                    IssueSeverity.ERROR,
                    entity_type,
                    entity_id,
                    f"Field '{field_name}' must not be empty",
                )
            )

    raw_type = fm.get("type")
    if raw_type is not None and safe_entity_type(raw_type) is None:
        issues.append(
            ValidationIssue(
                IssueCode.SCHEMA,
                IssueSeverity.ERROR,
                entity_type,
                entity_id,
                f"Field 'type' is not a valid entity type: {raw_type!r}",
            )
        )

    for field_name in ("created_at", "updated_at"):
        value = fm.get(field_name)
        if value is not None:
            try:
                datetime.fromisoformat(str(value))
            except ValueError:
                issues.append(
                    ValidationIssue(
                        IssueCode.SCHEMA,
                        IssueSeverity.ERROR,
                        entity_type,
                        entity_id,
                        f"Field '{field_name}' is not a valid datetime: {value!r}",
                    )
                )

    for field_name in LIST_FIELDS:
        value = fm.get(field_name)
        if value is not None and not isinstance(value, list):
            issues.append(
                ValidationIssue(
                    IssueCode.SCHEMA,
                    IssueSeverity.ERROR,
                    entity_type,
                    entity_id,
                    f"Field '{field_name}' must be a list",
                )
            )

    return issues
