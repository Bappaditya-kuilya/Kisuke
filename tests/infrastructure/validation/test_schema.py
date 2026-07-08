"""Tests for schema validation on raw frontmatter."""

from __future__ import annotations

from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.validation.report import IssueCode
from kisuke.infrastructure.validation.schema import schema_issues

TS = "2024-01-01T00:00:00+00:00"

VALID_MISSION = {
    "id": "11111111-1111-1111-1111-111111111111",
    "type": "mission",
    "title": "M",
    "owner": "kisuke-core",
    "status": "Active",
    "tags": [],
    "references": [],
    "attachments": [],
    "created_at": TS,
    "updated_at": TS,
}


def _codes(fm: dict) -> list[str]:
    return [i.code.value for i in schema_issues(fm, EntityType.MISSION)]


def test_valid_frontmatter_has_no_issues() -> None:
    assert schema_issues(VALID_MISSION, EntityType.MISSION) == []


def test_missing_required_field() -> None:
    fm = dict(VALID_MISSION)
    del fm["title"]
    issues = schema_issues(fm, EntityType.MISSION)
    assert any(i.code == IssueCode.SCHEMA and "title" in i.message for i in issues)


def test_invalid_uuid() -> None:
    fm = dict(VALID_MISSION)
    fm["id"] = "not-a-uuid"
    issues = schema_issues(fm, EntityType.MISSION)
    assert any(i.code == IssueCode.SCHEMA and "id" in i.message for i in issues)


def test_invalid_type() -> None:
    fm = dict(VALID_MISSION)
    fm["type"] = "widget"
    issues = schema_issues(fm, EntityType.MISSION)
    assert any(i.code == IssueCode.SCHEMA and "type" in i.message for i in issues)


def test_bad_timestamp() -> None:
    fm = dict(VALID_MISSION)
    fm["created_at"] = "yesterday"
    issues = schema_issues(fm, EntityType.MISSION)
    assert any(i.code == IssueCode.SCHEMA and "created_at" in i.message for i in issues)


def test_non_list_field() -> None:
    fm = dict(VALID_MISSION)
    fm["tags"] = "not-a-list"
    issues = schema_issues(fm, EntityType.MISSION)
    assert any(i.code == IssueCode.SCHEMA and "tags" in i.message for i in issues)


def test_empty_owner_rejected() -> None:
    fm = dict(VALID_MISSION)
    fm["owner"] = ""
    issues = schema_issues(fm, EntityType.MISSION)
    assert any(i.code == IssueCode.SCHEMA and "owner" in i.message for i in issues)
