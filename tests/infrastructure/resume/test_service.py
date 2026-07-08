"""Context reconstruction, graph traversal, next-action, and validation tests."""

from __future__ import annotations

from pathlib import Path

from kisuke.domain.entities import Task
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import MissionStatus, TaskStatus
from kisuke.domain.owner import Owner
from kisuke.infrastructure.resume.model import ResumeResult
from kisuke.infrastructure.resume.service import ResumeService
from kisuke.infrastructure.search.api import SearchEngine
from tests.infrastructure.resume.conftest import (
    MTG,
    MTG2,
    P2,
    PERS,
    REV,
    T1,
    T2,
    TS,
    D,
    K,
    M,
    P,
    R,
)


def test_context_reconstruction(working_repo: Path) -> None:
    result = ResumeService(working_repo).resume()
    assert result.mission is not None and str(result.mission.id) == M
    assert result.project is not None and str(result.project.id) == P
    assert result.next_action is not None and str(result.next_action.id) == T1
    assert {str(t.id) for t in result.related_tasks} == {T1, T2}
    assert {str(k.id) for k in result.knowledge} == {K}
    assert {str(d.id) for d in result.decisions} == {D}
    assert {str(m.id) for m in result.meetings} == {MTG, MTG2}
    assert {str(r.id) for r in result.resources} == {R}
    assert {str(p.id) for p in result.people} == {PERS}
    assert {str(rv.id) for rv in result.reviews} == {REV}
    assert "Weekly: Completed (2024-01-07)" in result.review_status_summary()


def test_graph_traversal_includes_relationship_meetings(working_repo: Path) -> None:
    # MTG2 references the project but is not in project.meetings.
    result = ResumeService(working_repo).resume()
    assert {str(m.id) for m in result.meetings} == {MTG, MTG2}


def test_next_action_resolved(working_repo: Path) -> None:
    result = ResumeService(working_repo).resume()
    assert result.next_action is not None
    assert str(result.next_action.id) == T1


def test_next_action_absent_when_unset(working_repo: Path) -> None:
    result = ResumeService(working_repo).resume(focus_project=P2)
    assert result.project is not None and str(result.project.id) == P2
    assert result.next_action is None


def test_resume_uses_focus_override(working_repo: Path) -> None:
    result = ResumeService(working_repo).resume(focus_project=P2)
    assert str(result.project.id) == P2


def test_resume_from_search(working_repo: Path) -> None:
    search = SearchEngine(working_repo / "search.db")
    search.rebuild(working_repo)
    service = ResumeService(working_repo, search)
    result = service.resume_from_search("Build Kisuke")
    assert result is not None
    assert str(result.project.id) == P


def test_resume_from_search_miss_returns_none(working_repo: Path) -> None:
    search = SearchEngine(working_repo / "search.db")
    search.rebuild(working_repo)
    service = ResumeService(working_repo, search)
    assert service.resume_from_search("zzzno-such-term") is None


def test_resume_from_search_requires_engine(working_repo: Path) -> None:
    import pytest

    service = ResumeService(working_repo)
    with pytest.raises(RuntimeError):
        service.resume_from_search("Build Kisuke")


def test_focus_mission_override(working_repo: Path) -> None:
    # A second mission with its own active project to confirm override routing.
    from kisuke.domain.entities import Mission as MType
    from kisuke.infrastructure.storage.repository import FileRepository

    repo = FileRepository(working_repo)
    other = MType(
        id=EntityId.from_string("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        title="Other Mission",
        owner=Owner.kisuke_core(),
        status=MissionStatus.PLANNING,
        created_at=TS,
        updated_at=TS,
    )
    repo.save(other)
    focus_id = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    result = ResumeService(working_repo).resume(focus_mission=focus_id)
    assert str(result.mission.id) == focus_id


def test_no_modification(working_repo: Path) -> None:
    before = sorted(p.read_bytes() for p in working_repo.rglob("*.md"))
    ResumeService(working_repo).resume()
    after = sorted(p.read_bytes() for p in working_repo.rglob("*.md"))
    assert before == after


def test_validation_reports_next_action_inconsistency(working_repo: Path) -> None:
    task_a = Task(
        id=EntityId.from_string(T1),
        title="A",
        owner=Owner.of(EntityId.from_string(P)),
        status=TaskStatus.TODO,
        created_at=TS,
        updated_at=TS,
    )
    task_b = Task(
        id=EntityId.from_string(T2),
        title="B",
        owner=Owner.of(EntityId.from_string(P)),
        status=TaskStatus.TODO,
        created_at=TS,
        updated_at=TS,
    )
    result = ResumeResult(related_tasks=[task_b], next_action=task_a)
    problems = ResumeService(working_repo).validate(result)
    assert any("next action" in p.lower() for p in problems)
