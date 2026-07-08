"""Additional relationship and ownership edge-case validation tests."""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.validation.report import IssueCode
from kisuke.infrastructure.validation.validator import RepositoryValidator
from tests.infrastructure.validation.conftest import TS, write_fm

M = "11111111-1111-1111-1111-111111111111"
T = "33333333-3333-3333-3333-333333333333"
MISSING = "99999999-9999-9999-9999-999999999999"
NOPE = "77777777-7777-7777-7777-777777777777"


def _mission(id: str = M) -> dict:
    return {
        "id": id,
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


def _project(owner: str, **extra: object) -> dict:
    base = {
        "id": "22222222-2222-2222-2222-222222222222",
        "type": "project",
        "title": "P",
        "owner": owner,
        "status": "Active",
        "priority": None,
        "next_action": None,
        "tasks": [],
        "knowledge": [],
        "decisions": [],
        "meetings": [],
        "resources": [],
        "people": [],
        "tags": [],
        "references": [],
        "attachments": [],
        "created_at": TS,
        "updated_at": TS,
    }
    base.update(extra)
    return base


def test_duplicate_typed_reference(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission())
    write_fm(tmp_path, "project", "p.md", _project(M, tasks=[T, T]))
    report = RepositoryValidator(tmp_path).validate()
    assert any(
        i.code == IssueCode.INVALID_REFERENCE and "Duplicate reference" in i.message
        for i in report.issues
    )


def test_owner_sentinel_rejected_for_project(tmp_path: Path) -> None:
    write_fm(tmp_path, "project", "p.md", _project("independent"))
    report = RepositoryValidator(tmp_path).validate()
    ownership = report.by_code(IssueCode.OWNERSHIP)
    assert any(i.entity_id == "22222222-2222-2222-2222-222222222222" for i in ownership)


def test_owner_references_missing_entity(tmp_path: Path) -> None:
    write_fm(tmp_path, "project", "p.md", _project(NOPE))
    report = RepositoryValidator(tmp_path).validate()
    ownership = report.by_code(IssueCode.OWNERSHIP)
    assert any(NOPE in i.message for i in ownership)


def test_duplicate_generic_reference(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission())
    write_fm(tmp_path, "project", "p.md", _project(M, references=[MISSING, MISSING]))
    report = RepositoryValidator(tmp_path).validate()
    # Only one orphan (the duplicate is skipped).
    assert len(report.by_code(IssueCode.ORPHAN_REFERENCE)) == 1


def test_attachment_orphan(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission())
    write_fm(tmp_path, "project", "p.md", _project(M, attachments=[MISSING]))
    report = RepositoryValidator(tmp_path).validate()
    assert report.by_code(IssueCode.ORPHAN_REFERENCE)


def test_attachment_wrong_type(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission())
    write_fm(tmp_path, "project", "p.md", _project(M, attachments=[M]))
    report = RepositoryValidator(tmp_path).validate()
    assert report.by_code(IssueCode.INVALID_REFERENCE)


def test_next_action_orphan(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission())
    write_fm(tmp_path, "project", "p.md", _project(M, next_action=MISSING))
    report = RepositoryValidator(tmp_path).validate()
    assert report.by_code(IssueCode.ORPHAN_REFERENCE)


def test_next_action_wrong_type(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission())
    write_fm(tmp_path, "project", "p.md", _project(M, next_action=M))
    report = RepositoryValidator(tmp_path).validate()
    assert report.by_code(IssueCode.INVALID_REFERENCE)


def test_malformed_owner_is_parse_error(tmp_path: Path) -> None:
    write_fm(tmp_path, "project", "p.md", _project("bogus"))
    report = RepositoryValidator(tmp_path).validate()
    assert report.by_code(IssueCode.PARSE_ERROR)
