"""Performance benchmark for integration synchronization.

Measures baseline (full incremental update) and incremental (single-file change)
synchronization latency over a populated repository. Pure local operation, no
network. Prints timings so they can be transcribed into BENCHMARK.md.
"""

from __future__ import annotations

import time
from pathlib import Path

from kisuke.application.entities import build_entity
from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.storage.repository import FileRepository
from kisuke.integrations import SyncService
from tests.integrations.conftest import make_populated


def test_sync_performance(repo_root: Path, data_dir: Path) -> None:
    ids = make_populated(repo_root)
    repo = FileRepository(repo_root)
    for i in range(200):
        task = build_entity(EntityType.TASK, {"title": f"Task {i}", "project": ids[1]})
        repo.save(task)

    db = data_dir / "index.db"
    cache = data_dir / ".cache"
    service = SyncService(repo_root, db, cache)

    start = time.perf_counter()
    baseline = service.sync_incremental()
    baseline_ms = (time.perf_counter() - start) * 1000.0

    task_file = repo_root / "tasks" / f"{ids[2]}.md"
    task_file.write_text(
        task_file.read_text(encoding="utf-8") + "\n<!-- benchmark edit -->\n",
        encoding="utf-8",
    )

    start = time.perf_counter()
    incremental = service.sync_incremental()
    incremental_ms = (time.perf_counter() - start) * 1000.0

    print("\nSYNC BENCHMARK")
    print(f"  entities            : {baseline.indexed}")
    print(f"  baseline update     : {baseline_ms:.1f} ms")
    print(f"  incremental update  : {incremental_ms:.1f} ms")

    assert baseline.baseline is True
    assert baseline.indexed >= 203
    assert any(c.kind == "modified" for c in incremental.changes)
