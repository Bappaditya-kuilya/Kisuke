# M4 Verification Report — Search Engine

> Milestone: M4 (Search) of the canonical order
> Repository → Domain → Storage → Parser & Validation → **Search** → Resume → CLI → Reviews → Integrations → AI → Plugins → Polish
> Status: Implementation complete, awaiting approval to proceed to M5.

---

## Scope

Implemented the local, offline Search engine in the Infrastructure layer. It
builds a SQLite inverted index from the Markdown repository, supports free-text
search, exact-ID lookup, and filtering by type/owner/status, with deterministic
ranking and incremental (rebuildable) indexing. No external search engine, no
network, no Storage/Validation behavior changes (those modules are reused
directly). Implementation derives from `docs/engineering/12-engineering-architecture.md`
(Search Architecture: Markdown → Indexer → SQLite Index → Search Engine).

---

## Files Added

| File | Purpose |
|------|---------|
| `src/kisuke/infrastructure/search/__init__.py` | Package exports |
| `src/kisuke/infrastructure/search/model.py` | `SearchResult` dataclass |
| `src/kisuke/infrastructure/search/ranking.py` | `tokenize`, field weights, `sort_results` (deterministic) |
| `src/kisuke/infrastructure/search/index.py` | `IndexBuilder` + `hash_content` (SQLite inverted index, content-hash change detection) |
| `src/kisuke/infrastructure/search/api.py` | `SearchEngine` (rebuild / update / search / get_by_id) |
| `tests/infrastructure/search/__init__.py` | Test package |
| `tests/infrastructure/search/conftest.py` | Fixtures: valid repo, filter repo, benchmark repo |
| `tests/infrastructure/search/test_ranking.py` | Tokenization + deterministic ranking |
| `tests/infrastructure/search/test_search.py` | Indexing, full-text, filters, exact lookup, integrity |
| `tests/infrastructure/search/test_incremental_bench.py` | Incremental updates + performance benchmark |
| `reports/m4-coverage.txt` | Coverage report |
| `htmlcov/` | HTML coverage |

---

## Milestone Scope Coverage

| # | Scope item | Where |
|---|-----------|-------|
| 1 | Local search index | `index.IndexBuilder` (SQLite) |
| 2 | Incremental indexing | `api.SearchEngine.update` (content-hash skip) |
| 3 | Entity indexing | `index.IndexBuilder.upsert` (title/tag/body tokens) |
| 4 | Full-text search | `api.SearchEngine.search` + `tokens` table |
| 5 | Metadata filtering | `search` WHERE clauses: type/owner/status |
| 6 | Ranking | `ranking.field_weight` + `ranking.sort_results` |
| 7 | Exact ID lookup | `api.SearchEngine.get_by_id` |
| 8 | Type filtering | `search(type=...)` |
| 9 | Search result model | `model.SearchResult` |
| 10 | Index rebuild | `api.SearchEngine.rebuild` |

---

## Requirements Check

- **Markdown remains canonical** — index is derived; source files are never written by the search engine.
- **Index fully rebuildable** — `rebuild()` drops and reconstructs from Markdown (`test_index_is_rebuildable`, `test_index_integrity_matches_repo`).
- **Incremental only updates changed entities** — `update()` compares a SHA-256 content hash; unchanged entities are skipped (`test_incremental_skips_unchanged`), changed ones re-indexed (`test_incremental_detects_change`), deleted ones removed (`test_incremental_removes_deleted`).
- **Exact ID lookup** — `get_by_id` (`test_exact_id_lookup`).
- **Free-text search** — `search(query)` over title/tag/body tokens (`test_full_text_search`).
- **Filter by type / owner / status** — `test_type_filter`, `test_owner_filter`, `test_status_filter`.
- **Deterministic ranking** — title > tag > body weights, tie-broken by title then id (`test_title_match_ranks_above_body`, `test_sort_results_*`).
- **No external search engine / no network** — pure SQLite + Python stdlib, no imports beyond `sqlite3`/stdlib/domain/infrastructure.
- **SQLite as local index** — used.

---

## Verification Results

| Check | Result |
|-------|--------|
| Ruff (`ruff check .`) | All checks passed |
| MyPy (`mypy`, strict) | Success: no issues found in 35 source files |
| Pytest | 157 passed |
| Coverage | 98% (TOTAL 1181 stmts, 27 missed); search package 96–100% |
| Architecture deviations | None |

---

## Benchmark Summary

Measured on a repository of **500 entities** (1 mission, 1 project, 498 tasks):

| Operation | Time |
|-----------|------|
| Full rebuild | ~103 ms |
| Incremental update (no changes) | ~27 ms |
| Average free-text search | ~6.8 ms (over 100 runs) |

- Incremental update is **~3.8× faster** than full rebuild (confirms incremental requirement).
- Typical search latency (**6.8 ms**) is far below the **500 ms** target.
- `test_benchmark_performance` asserts: `update_time < rebuild_time` and `avg_search < 0.5 s`.

---

## LOC

| Metric | Count |
|--------|-------|
| Production LOC (`src/kisuke/infrastructure/search/`) | 317 |
| Test LOC (`tests/infrastructure/search/`) | 304 |

---

## Test Inventory (157 tests)

- **Ranking (5):** tokenization, field-weight ordering, deterministic sort by score/title/id.
- **Search (11):** rebuild populates, exact ID lookup, full-text, type/owner/status filters, empty query, title-rank-above-body, rebuildable, integrity matches repo.
- **Incremental/Benchmark (4):** skip unchanged, detect change, remove deleted, performance benchmark.

---

## Notes / Design Decisions

- **Self-contained inverted index.** A manual token → `(entity_id, field)` table in SQLite provides full-text search without FTS5 or any external engine, satisfying "no external search engine" unambiguously and remaining fully deterministic.
- **Incremental via content hash.** Each indexed entity stores a SHA-256 of its Markdown; `update()` re-indexes only entities whose hash changed and prunes entities whose files disappeared. This is robust to mtime/clock quirks.
- **No Storage/Validation changes.** The engine reuses `RepositoryScanner` and `IncrementalParser` from the validation package and `split_markdown` from storage — integration points only.
- **Ranking is transparent.** Score = Σ token-weight (title 5, tag 3, body 1); ties broken by title then id. No opaque scoring model.

---

## Exit Criteria (per roadmap M4)

- Full-text search tests: **PASS**
- Incremental index tests: **PASS**
- Ranking tests: **PASS**
- Rebuild tests: **PASS**
- Performance benchmark: **PASS**
- Index integrity tests: **PASS**
- Ruff: **PASS**
- MyPy (strict): **PASS**
- Pytest: **PASS**

**Result: PASS.** Awaiting approval before starting M5 (Resume).
