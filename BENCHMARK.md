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
