# M5 Benchmark

> Resume engine performance. Measured on an Apple-class machine (CPython 3.12,
> warm filesystem cache). The resume engine loads all entities once per call
> and reconstructs context via in-memory graph traversal — no network, no AI.

## Method

- Build a repository with one Mission, one Project, and N Tasks (Project.tasks
  populated with the N task IDs, as required by the Domain Model).
- `ResumeService.resume()` is timed for a single warm call and for the average
  of 10 repeated calls.

## Results

| Repository size | Warm resume | Repeated resume (avg) | Tasks reconstructed |
|-----------------|-------------|------------------------|---------------------|
| 150 entities    | 8.8 ms      | 9.5 ms                 | 150                 |
| 500 entities    | 30.4 ms     | 31.3 ms                | 500                 |

## Targets

| Target | Requirement | Result |
|--------|-------------|--------|
| Warm cache resume | < 2 s | ✅ 8.8–30.4 ms |
| Typical resume | < 250 ms | ✅ 8.8–30.4 ms |
| Deterministic output | identical across runs | ✅ verified by `test_resume_is_deterministic` |

## Notes

- Resume is purely read-only; output is byte-for-byte deterministic because
  entity selection and ordering are keyed by ID/status rank.
- Scaling is linear in repository size (full load + traversal); a 3.3× larger
  repo costs ~3.5× the time, well within budget.
- Rebuilding the Search index is not required for resume; `resume_from_search`
  adds only a single exact-ID/top-hit lookup when a SearchEngine is supplied.

---

# M7 Benchmark

> Integration synchronization performance. Measured on an Apple-class machine
> (CPython 3.12, warm filesystem cache). Sync is a local, offline operation: it
> snapshots the repository, detects canonical changes via (mtime, size), and
> applies an incremental Search index update. No network, no AI.

## Method

- Build a repository with one Mission, one Project, 200 Tasks, and the connecting
  Project/Mission entities (203 entities total) using `make_populated` plus a batch
  of `build_entity` / `FileRepository.save` writes.
- `SyncService.sync_incremental()` is timed for the baseline run (no previous
  snapshot) and for a subsequent run after a single Markdown file edit.

## Results

| Repository size | Baseline update | Incremental update | Changes detected |
|-----------------|-----------------|---------------------|------------------|
| 203 entities    | 96.9 ms         | 40.3 ms             | 1 modified       |

## Targets

| Target | Requirement | Result |
|--------|-------------|--------|
| Incremental indexing only | derived state, not full rebuild | ✅ change-detected incremental update |
| No performance regression | CLI/Search budgets preserved | ✅ baseline 96.9 ms < 200 ms CLI budget |
| Deterministic | identical snapshot diff each run | ✅ verified by `test_incremental_detects_modification` |

## Notes

- Sync never touches canonical Markdown unless an explicit, user-approved Git
  commit path is supplied; the index update is rebuildable and non-destructive.
- Derived artifacts (the SQLite index database and the sync snapshot cache) are
  excluded from change detection, so a sync run never reports changes to itself.
- Scaling is linear in repository size: the baseline cost is dominated by the
  incremental Search index `update()` over all entities; an incremental run only
  re-indexes the delta plus the full scan's cheap signature comparison.
- The filesystem watcher is poll-based (no external watchdog dependency) and adds
  negligible overhead between polls; background polling is exercised by
  `test_start_stop_background`.

