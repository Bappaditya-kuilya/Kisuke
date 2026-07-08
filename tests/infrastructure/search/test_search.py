"""Tests for the search engine: indexing, full-text, filters, exact lookup."""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.search.api import SearchEngine
from tests.infrastructure.search.conftest import (
    _full,
    _md,
    make_all,
)

PROJECT_ID = "20000000-0000-0000-0000-000000000000"


def test_rebuild_populates_index(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        assert len(eng.builder.all_ids()) == 11


def test_exact_id_lookup(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        result = eng.get_by_id(PROJECT_ID)
        assert result is not None
        assert result.entity_type == "project"
        assert "Kisuke" in result.title


def test_full_text_search(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        results = eng.search("Kisuke")
        assert results
        assert any(r.entity_type == "project" for r in results)


def test_type_filter(filter_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(filter_repo)
        results = eng.search("shared", type="mission")
        assert len(results) == 1
        assert results[0].entity_type == "mission"


def test_owner_filter(filter_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(filter_repo)
        results = eng.search("shared", owner="kisuke-core")
        assert len(results) == 2
        assert all(r.owner == "kisuke-core" for r in results)


def test_status_filter(filter_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(filter_repo)
        results = eng.search("shared", status="Active")
        assert len(results) == 3


def test_empty_query_returns_empty(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        assert eng.search("   ") == []


def test_title_match_ranks_above_body(tmp_path: Path) -> None:
    _md("mission", "a.md", _full(
        id="11111111-1111-1111-1111-111111111111", type="mission",
        title="targetword alpha", owner="kisuke-core", status="Active",
    ), "", tmp_path)
    _md("mission", "b.md", _full(
        id="22222222-2222-2222-2222-222222222222", type="mission",
        title="Other title", owner="kisuke-core", status="Active",
    ), "targetword beta body text", tmp_path)
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(tmp_path)
        results = eng.search("targetword")
        assert len(results) == 2
        assert results[0].entity_id == "11111111-1111-1111-1111-111111111111"


def test_index_is_rebuildable(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        first = len(eng.builder.all_ids())
        eng.rebuild(valid_repo)
        assert len(eng.builder.all_ids()) == first == 11


def test_index_integrity_matches_repo(valid_repo: Path, tmp_path: Path) -> None:
    with SearchEngine(tmp_path / "s.db") as eng:
        eng.rebuild(valid_repo)
        expected = {str(e.id) for e in make_all()}
        assert eng.builder.all_ids() == expected
        for entity_id in expected:
            assert eng.get_by_id(entity_id) is not None
