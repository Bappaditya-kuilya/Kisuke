"""Tests for ranking and tokenization."""

from __future__ import annotations

from kisuke.infrastructure.search.model import SearchResult
from kisuke.infrastructure.search.ranking import (
    field_weight,
    sort_results,
    tokenize,
)


def test_tokenize_lowercases_and_splits() -> None:
    assert tokenize("Build Kisuke! alpha_beta") == ["build", "kisuke", "alpha_beta"]


def test_tokenize_empty() -> None:
    assert tokenize("") == []
    assert tokenize("   ") == []


def test_field_weight_ordering() -> None:
    assert field_weight("title") > field_weight("tag") > field_weight("body")


def test_sort_results_deterministic() -> None:
    results = [
        SearchResult("b", "task", "Beta", "o", "Todo", 1.0),
        SearchResult("a", "task", "Alpha", "o", "Todo", 2.0),
        SearchResult("c", "task", "Gamma", "o", "Todo", 2.0),
    ]
    ordered = sort_results(results)
    assert [r.entity_id for r in ordered] == ["a", "c", "b"]


def test_sort_results_by_score_then_title() -> None:
    results = [
        SearchResult("x", "task", "Zed", "o", "Todo", 1.0),
        SearchResult("y", "task", "Abe", "o", "Todo", 5.0),
    ]
    ordered = sort_results(results)
    assert ordered[0].entity_id == "y"
