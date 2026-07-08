"""Ordering, determinism, and performance benchmark tests."""

from __future__ import annotations

import time
from pathlib import Path

from kisuke.infrastructure.resume.ordering import order_entities
from kisuke.infrastructure.resume.service import ResumeService
from tests.infrastructure.resume.conftest import T1, T2, TS


def test_related_tasks_ordered_by_status_then_id(working_repo: Path) -> None:
    result = ResumeService(working_repo).resume()
    # T1 is In Progress (rank 0); T2 is Todo (rank 1) -> T1 first.
    assert [str(t.id) for t in result.related_tasks] == [T1, T2]


def test_order_entities_deterministic() -> None:
    from kisuke.domain.entities import Task
    from kisuke.domain.ids import EntityId
    from kisuke.domain.lifecycle import TaskStatus
    from kisuke.domain.owner import Owner

    owner = Owner.of(EntityId.from_string("22222222-2222-2222-2222-222222222222"))
    a = Task(
        id=EntityId.from_string(T2),
        title="a",
        owner=owner,
        status=TaskStatus.TODO,
        created_at=TS,
        updated_at=TS,
    )
    b = Task(
        id=EntityId.from_string(T1),
        title="b",
        owner=owner,
        status=TaskStatus.IN_PROGRESS,
        created_at=TS,
        updated_at=TS,
    )
    ordered = order_entities([a, b])
    assert [str(t.id) for t in ordered] == [T1, T2]


def test_resume_is_deterministic(working_repo: Path) -> None:
    service = ResumeService(working_repo)
    first = service.resume()
    second = service.resume()
    assert first == second
    assert first.summary() == second.summary()
    assert first.to_dict() == second.to_dict()


def test_resume_benchmark(bench_repo: Path) -> None:
    service = ResumeService(bench_repo)
    # Warm run.
    t0 = time.perf_counter()
    result = service.resume()
    warm = time.perf_counter() - t0
    # Repeated runs must be deterministic and fast.
    for _ in range(5):
        assert service.resume() == result
    assert warm < 2.0
    assert warm < 0.25
