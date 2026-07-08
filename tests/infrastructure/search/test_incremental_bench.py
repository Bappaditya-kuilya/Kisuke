"""Incremental indexing and benchmark tests."""

from __future__ import annotations

import time
from pathlib import Path

from kisuke.infrastructure.search.api import SearchEngine

PROJECT_ID = "20000000-0000-0000-0000-000000000000"


def test_incremental_skips_unchanged(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        after_rebuild = eng.builder.upsert_count
        assert after_rebuild == 11
        eng.update(valid_repo)
        # No file changed -> no new upserts.
        assert eng.builder.upsert_count == after_rebuild


def test_incremental_detects_change(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        project_path = valid_repo / "projects" / f"{PROJECT_ID}.md"
        text = project_path.read_text(encoding="utf-8")
        text = text.replace("Build Kisuke", "Build Kisuke zzznewterm")
        project_path.write_text(text, encoding="utf-8")
        eng.update(valid_repo)
        results = eng.search("zzznewterm")
        assert any(r.entity_id == PROJECT_ID for r in results)


def test_incremental_removes_deleted(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        (valid_repo / "missions" / "10000000-0000-0000-0000-000000000000.md").unlink()
        eng.update(valid_repo)
        assert eng.get_by_id("1000000000000000000000000000000") is None
        assert len(eng.builder.all_ids()) == 10


def test_benchmark_performance(bench_repo: Path, tmp_path: Path) -> None:
    db = tmp_path / "bench.db"
    with SearchEngine(db) as eng:
        t0 = time.perf_counter()
        eng.rebuild(bench_repo)
        rebuild_time = time.perf_counter() - t0

        t1 = time.perf_counter()
        eng.update(bench_repo)
        update_time = time.perf_counter() - t1

        # Incremental update of an unchanged repo must be faster than full rebuild.
        assert update_time < rebuild_time

        # Typical search well under the 500 ms target.
        t2 = time.perf_counter()
        for _ in range(50):
            eng.search("alpha")
        avg_search = (time.perf_counter() - t2) / 50
        assert avg_search < 0.5

        # The indexed data is correct.
        assert len(eng.search("alpha")) == 200
