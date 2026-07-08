# M7 Verification Report — Integrations

> Milestone M7: Integrations. Verified against docs/engineering/09-integrations.md,
> docs/execution/14-implementation-plan.md (Phase 8), and
> docs/engineering/12-engineering-architecture.md.

---

## Status

✅ Complete. All quality gates pass.

- Ruff: clean
- MyPy (strict): clean
- Pytest: all integration tests pass
- Coverage: 94% (integrations + plugins), 95% (whole project)
- Architecture deviations: **None**

---

## Scope Coverage (all 10 items delivered)

| # | Scope item | Module | Notes |
|---|------------|--------|-------|
| 1 | Integration interface | `src/kisuke/plugins/interfaces.py` | `Integration` ABC + `IntegrationInfo` |
| 2 | Plugin registry | `src/kisuke/plugins/registry.py` | discover, enable/disable, options, JSON persistence |
| 3 | Git integration | `src/kisuke/integrations/git.py` | read-only introspection + explicit commit |
| 4 | Filesystem watcher | `src/kisuke/integrations/watcher.py` | poll-based, callback, background thread |
| 5 | Markdown import | `src/kisuke/integrations/markdown_import.py` | additive, safe, validation-gated |
| 6 | Export interface | `src/kisuke/integrations/export.py` | bundle + JSON, read-only |
| 7 | Synchronization service | `src/kisuke/integrations/sync.py` | incremental index sync + optional Git commit |
| 8 | Change detection | `src/kisuke/integrations/change.py` | snapshot, diff, entity-ID mapping |
| 9 | Integration configuration | `src/kisuke/integrations/config.py` | enable/disable + options via registry |
| 10 | Integration tests | `tests/integrations/` | watcher, git, sync, change, export/import, config, bench |

---

## Files Added

Production (`src/kisuke/`):

- `src/kisuke/plugins/interfaces.py`
- `src/kisuke/plugins/registry.py`
- `src/kisuke/plugins/__init__.py`
- `src/kisuke/integrations/__init__.py`
- `src/kisuke/integrations/base.py`
- `src/kisuke/integrations/change.py`
- `src/kisuke/integrations/config.py`
- `src/kisuke/integrations/export.py`
- `src/kisuke/integrations/git.py`
- `src/kisuke/integrations/markdown_import.py`
- `src/kisuke/integrations/sync.py`
- `src/kisuke/integrations/watcher.py`

Tests (`tests/integrations/`):

- `tests/integrations/conftest.py`
- `tests/integrations/test_registry.py`
- `tests/integrations/test_change.py`
- `tests/integrations/test_git.py`
- `tests/integrations/test_watcher.py`
- `tests/integrations/test_sync.py`
- `tests/integrations/test_export_import.py`
- `tests/integrations/test_config.py`
- `tests/integrations/test_bench.py`

---

## Metrics

| Metric | Value |
|--------|-------|
| Production LOC (integrations + plugins) | 895 |
| Test LOC (integrations) | 640 |
| Coverage — integrations + plugins | 94% |
| Coverage — whole project | 95% |

### Per-module coverage (integrations + plugins)

| Module | Lines | Missed | Coverage |
|--------|-------|--------|---------|
| integrations/__init__.py | 24 | 0 | 100% |
| integrations/base.py | 10 | 0 | 100% |
| integrations/change.py | 65 | 0 | 100% |
| integrations/config.py | 28 | 0 | 100% |
| integrations/export.py | 45 | 0 | 100% |
| integrations/git.py | 53 | 4 | 92% |
| integrations/markdown_import.py | 45 | 3 | 93% |
| integrations/sync.py | 70 | 9 | 87% |
| integrations/watcher.py | 40 | 1 | 98% |
| plugins/__init__.py | 4 | 0 | 100% |
| plugins/interfaces.py | 20 | 1 | 95% |
| plugins/registry.py | 84 | 9 | 89% |

HTML coverage report: `reports/htmlcov-m7/`

---

## Ruff Result

```
All checks passed!
```

Configuration: `select = ["E", "F", "I", "W", "UP", "B"]`, line-length 100, py312.

---

## MyPy Result

```
Success: no issues found in 65 source files
```

Configuration: `strict = true`, `python_version = "3.12"`, `files = ["src"]`.

---

## Pytest Result

```
tests/integrations  .......................................   39 passed
```

All integration suites pass:

- `test_registry.py` — plugin interface + registry (discovery, persistence, options)
- `test_change.py` — change detection, `.git` exclusion, derived-ignore, entity-ID mapping
- `test_git.py` — git integration (graceful degradation, commit, status, branch)
- `test_watcher.py` — filesystem watcher (added/modified/removed, callback, thread, ignore)
- `test_sync.py` — incremental sync, derived-artifact exclusion, Git commit path
- `test_export_import.py` — read-only export, safe additive import
- `test_config.py` — integration configuration facade
- `test_bench.py` — synchronization performance benchmark

---

## Benchmark Summary

Measured on a 203-entity repository (whole-project, warm cache, CPython 3.12):

| Run | Latency | Notes |
|-----|---------|-------|
| Baseline sync (no prior snapshot) | 96.9 ms | full incremental index `update()` |
| Incremental sync (1 file edited) | 40.3 ms | change-detected delta |

- Incremental indexing only — no full rebuild; derived artifacts are excluded from
  change detection so a sync never reports changes to its own index/cache.
- Baseline (96.9 ms) stays under the 200 ms CLI startup budget; no regression.
- Full results in `BENCHMARK.md` (M7 section).

---

## Acceptance Criteria (docs/engineering/09-integrations.md § Acceptance)

| Criterion | Result |
|-----------|--------|
| Core works without integrations | ✅ Integrations are adapters; `Domain`/`Storage`/`Search`/`Resume`/`CLI` are untouched and tests pass without any integration enabled |
| Every integration is optional | ✅ Built-ins register but default disabled; no integration is imported by core paths |
| Providers are replaceable | ✅ `Integration` ABC + `PluginRegistry` discovery; swap via public interface |
| Markdown remains canonical | ✅ Export is read-only; import is additive and validation-gated; sync never mutates canonical Markdown except an explicit, user-approved Git commit |
| No integration owns Kisuke data | ✅ Registry persists only enable/options state; integrations store nothing canonical |

---

## Architecture Deviations

**None.**

Dependencies point inward (Integrations → Infrastructure/Domain public interfaces).
Integrations are adapters only; the Domain layer was not modified. No AI. No network
requirement for core functionality. Git remains the system of record. Filesystem
changes trigger incremental updates via the watcher + sync service. Plugin architecture
(`plugins/`) is respected; no vendor lock-in.

---

## Bugs Found and Fixed During M7

1. `Integration.configure` was `@abstractmethod`, preventing minimal plugins that
   subclass `Integration` directly (without a `configure` body) from instantiating;
   the registry silently swallowed the error during discovery. Fixed by giving
   `Integration.configure` a default no-op body.
2. `PluginRegistry.enable`/`disable`/`set_option` required a live registration, so
   persisted enable/disable state could not be toggled after a config-only reload.
   Fixed to also accept names present in persisted state.
3. `GitIntegration.status` treated the `## branch` porcelain header as a change,
   falsely reporting a dirty tree. Fixed by skipping `## ` header lines.
4. `change.snapshot` included derived artifacts (SQLite index, sync cache) and the
   `.git` tree, polluting change detection. Fixed by always excluding `.git` and
   accepting an `ignore` set; `SyncService` now ignores its own index DB and cache.

---

## Verification Commands

```bash
ruff check src tests
mypy src
pytest tests/integrations --cov=src/kisuke/integrations --cov=src/kisuke/plugins \
      --cov-report=html:reports/htmlcov-m7
```
