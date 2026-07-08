"""Tests for the repository validator against corrupted and inconsistent repos."""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.validation.report import IssueCode
from kisuke.infrastructure.validation.validator import RepositoryValidator
from tests.infrastructure.validation.conftest import TS, write_fm

M = "11111111-1111-1111-1111-111111111111"
P0 = "22222222-2222-2222-2222-222222222222"
T = "33333333-3333-3333-3333-333333333333"
PB = "44444444-4444-4444-4444-444444444444"
MISSING = "99999999-9999-9999-9999-999999999999"

EMPTY_LISTS = {"tags": [], "references": [], "attachments": []}


def _mission(id: str, status: str = "Active") -> dict:
    return {
        "id": id, "type": "mission", "title": "M", "owner": "kisuke-core",
        "status": status, **EMPTY_LISTS, "created_at": TS, "updated_at": TS,
    }


def _project(id: str, owner: str, **extra: object) -> dict:
    base = {
        "id": id, "type": "project", "title": "P", "owner": owner,
        "status": "Active", "priority": None, "next_action": None,
        "tasks": [], "knowledge": [], "decisions": [], "meetings": [],
        "resources": [], "people": [], **EMPTY_LISTS,
        "created_at": TS, "updated_at": TS,
    }
    base.update(extra)
    return base


def _task(id: str, owner: str, **extra: object) -> dict:
    base = {
        "id": id, "type": "task", "title": "T", "owner": owner,
        "status": "Todo", "priority": None, "due_date": None, "estimated_time": None,
        **EMPTY_LISTS, "created_at": TS, "updated_at": TS,
    }
    base.update(extra)
    return base


def test_valid_repo_is_valid(valid_repo: Path) -> None:
    report = RepositoryValidator(valid_repo).validate()
    assert report.is_valid()
    assert report.errors() == []


def test_corrupted_repo_reports_schema_error(tmp_path: Path) -> None:
    fm = _mission(M)
    del fm["title"]
    write_fm(tmp_path, "mission", "a.md", fm)
    report = RepositoryValidator(tmp_path).validate()
    assert not report.is_valid()
    assert report.by_code(IssueCode.SCHEMA)


def test_duplicate_id_detected(tmp_path: Path) -> None:
    fm = _mission(M)
    write_fm(tmp_path, "mission", "a.md", fm)
    write_fm(tmp_path, "mission", "b.md", fm)
    report = RepositoryValidator(tmp_path).validate()
    dupes = report.by_code(IssueCode.DUPLICATE_ID)
    assert len(dupes) == 1
    assert dupes[0].entity_id == M


def test_orphan_reference_detected(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission(M))
    write_fm(tmp_path, "project", "p.md", _project(P0, M))
    write_fm(tmp_path, "task", "t.md", _task(T, P0, references=[MISSING]))
    report = RepositoryValidator(tmp_path).validate()
    orphans = report.by_code(IssueCode.ORPHAN_REFERENCE)
    assert any(i.entity_id == T for i in orphans)


def test_ownership_violation_detected(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission(M))
    write_fm(tmp_path, "project", "p0.md", _project(P0, M))
    write_fm(tmp_path, "task", "t.md", _task(T, P0))
    write_fm(tmp_path, "project", "pb.md", _project(PB, T))
    report = RepositoryValidator(tmp_path).validate()
    ownership = report.by_code(IssueCode.OWNERSHIP)
    assert any(i.entity_id == PB for i in ownership)
    assert all(i.code == IssueCode.OWNERSHIP for i in ownership)


def test_lifecycle_violation_detected(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission(M, status="Bogus"))
    report = RepositoryValidator(tmp_path).validate()
    lifecycle = report.by_code(IssueCode.LIFECYCLE)
    assert lifecycle
    assert lifecycle[0].entity_id == M


def test_invalid_reference_type_detected(tmp_path: Path) -> None:
    write_fm(tmp_path, "mission", "m.md", _mission(M))
    write_fm(tmp_path, "project", "p.md", _project(P0, M, tasks=[M]))
    report = RepositoryValidator(tmp_path).validate()
    invalid = report.by_code(IssueCode.INVALID_REFERENCE)
    assert any(i.entity_id == P0 for i in invalid)


def test_validation_is_read_only(valid_repo: Path) -> None:
    before = sorted(p.read_bytes() for p in valid_repo.rglob("*.md"))
    RepositoryValidator(valid_repo).validate()
    after = sorted(p.read_bytes() for p in valid_repo.rglob("*.md"))
    assert before == after


def test_results_are_deterministic(valid_repo: Path) -> None:
    first = RepositoryValidator(valid_repo).validate()
    second = RepositoryValidator(valid_repo).validate()
    assert [i.message for i in first.issues] == [i.message for i in second.issues]


def test_report_rendering(valid_repo: Path) -> None:
    import json

    report = RepositoryValidator(valid_repo).validate()
    text = report.render_text()
    assert "Status: VALID" in text
    data = json.loads(report.render_json())
    assert isinstance(data, list)
