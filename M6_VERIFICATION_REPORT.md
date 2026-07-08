# M6 Verification Report — Command Line Interface

> Milestone: M6 (CLI) of the canonical order
> Repository → Domain → Storage → Parser & Validation → Search → Resume → **CLI** → Reviews → Integrations → AI → Plugins → Polish
> Status: Implementation complete, awaiting approval to proceed to M7.

---

## Scope

Implemented the Kisuke CLI exactly as documented in `docs/engineering/08-cli-spec.md`.
The CLI is a thin adapter: every command delegates to an Application service, which
orchestrates the existing Infrastructure (Storage, Search, Resume, Validation) and
Domain layers. No business logic lives in the CLI. To honor the documented
architecture (Application sits between CLI and Domain), a new `application/` package
was added containing the use-case services the CLI delegates to.

---

## Files Added

| File | Purpose |
|------|---------|
| `src/kisuke/application/__init__.py` | Application package exports |
| `src/kisuke/application/workspace.py` | Repo-root resolution, `init`, `status` |
| `src/kisuke/application/entities.py` | `EntityService` + `build_entity`/`entity_to_dict` (create/list/show/archive/open) |
| `src/kisuke/application/tasks.py` | `TaskService` (add/list/next/done/move) |
| `src/kisuke/application/reviews.py` | `ReviewService` (morning/weekly/monthly/quarterly aggregation) |
| `src/kisuke/application/search_app.py` | `SearchService` (wraps `SearchEngine`) |
| `src/kisuke/application/resume_app.py` | `ResumeApp` (wraps `ResumeService` + last-focus persistence) |
| `src/kisuke/application/validation_app.py` | `ValidateService` (wraps `RepositoryValidator`) |
| `src/kisuke/application/index_app.py` | `IndexService` (build/update/clean) |
| `src/kisuke/application/config_app.py` | `ConfigService` + `resolve_config` |
| `src/kisuke/application/doctor.py` | `DoctorService` (repository/markdown/index/config/plugins checks) |
| `src/kisuke/application/plugins.py` | `PluginService` (local plugin registry) |
| `src/kisuke/cli/__init__.py` | CLI package export |
| `src/kisuke/cli/main.py` | `main()` entrypoint, dispatch, exit codes |
| `src/kisuke/cli/commands.py` | argparse command tree + handlers |
| `src/kisuke/cli/errors.py` | `ExitCode`, `CliError`, exception→exit-code mapping |
| `src/kisuke/cli/format.py` | `Result` + `OutputFormatter` (human / `--json`) |
| `src/kisuke/cli/completion.py` | Shell completion script generation (prepared) |
| `src/kisuke/__main__.py` | Console-script entry (`python -m kisuke`) |
| `tests/cli/__init__.py` | Test package |
| `tests/cli/conftest.py` | Isolated repo/data fixtures |
| `tests/cli/test_cli.py` | End-to-end CLI tests (commands, JSON, exit codes, help) |
| `tests/cli/test_snapshots.py` | Snapshot tests (completion, help, version) |
| `tests/cli/__snapshots__/*.txt` | Stored snapshots (6 files) |
| `tests/application/__init__.py` | Test package |
| `tests/application/test_app.py` | Application service unit tests |

---

## Milestone Scope Coverage

| # | Scope item | Where |
|---|-----------|-------|
| 1 | CLI framework | `cli/main.py`, `cli/commands.py` (argparse) |
| 2 | Global configuration | `application/config_app.py`, `workspace.resolve_repo_root` |
| 3 | Repository initialization | `workspace.init_repository` (`kisuke init`) |
| 4 | Mission commands | `mission create/list/show/archive` |
| 5 | Project commands | `project create/list/show/open/archive` |
| 6 | Task commands | `task add/list/next/done/move` |
| 7 | Knowledge commands | `knowledge add/list/open` |
| 8 | Cookbook commands | `cookbook add/search/open` |
| 9 | Decision commands | `decision add/list/show` |
| 10 | Meeting commands | `meeting add/today/list` |
| 11 | Person commands | `person add/list/show` |
| 12 | Resource commands | `resource add/list/open` |
| 13 | Review commands | `review morning/weekly/monthly/quarterly` |
| 14 | Search commands | `search <query>` with `--project/--cookbook/--knowledge/--decision/--resource/--person` |
| 15 | Resume commands | `resume` (`--mission/--project/--last`) |
| 16 | Validate commands | `validate` (Doctor-style repository validation) |
| 17 | Output formatting | `cli/format.py` (`--json` global flag, human default) |
| 18 | Error handling | `cli/errors.py` (consistent exit codes, helpful messages) |

---

## Requirements Check

- **Exactly the documented CLI** — 54 leaf commands matching `08-cli-spec.md`
  (init, doctor, status, config, resume, mission, project, task, knowledge,
  cookbook, decision, meeting, person, resource, review, search, sync, plugin,
  index; plus `completion` prepared per spec and `validate` per milestone scope #16).
- **No business logic in CLI** — handlers build parameter dicts and call Application
  services; all orchestration/ownership wiring lives in `application/`.
- **Every command delegates to Application/Infrastructure** — directly via
  `EntityService`, `TaskService`, `SearchService`, `ResumeApp`, `IndexService`,
  `ValidateService`, `DoctorService`, `PluginService`, `ConfigService`, `workspace`.
- **JSON output** — `--json` (accepted before or after the subcommand) emits
  machine-readable JSON for all commands.
- **Human-readable by default** — `OutputFormatter` prints prose unless `--json`.
- **Consistent exit codes** — `0 success, 1 general, 2 invalid args, 3 not found,
  4 validation, 5 permission`, centralized in `ExitCode`.
- **Helpful error messages** — errors print to stderr; not-found and validation
  failures carry the underlying message.
- **Shell completion prepared** — `completion --shell bash|zsh` generates a
  completion script (no runtime dependency, no network).
- **No network access** — all operations are local filesystem / SQLite.
- **No AI** — none implemented.
- **Architecture preserved** — Domain, Storage, Validation, Search, Resume behavior
  used only through their public APIs; nothing modified.

---

## Verification Results

| Check | Result |
|-------|--------|
| Ruff (`ruff check src/ tests/`) | All checks passed |
| MyPy (`mypy`, strict) | Success: no issues found in 55 source files |
| Pytest | All tests passed (full suite) |
| Coverage (application + cli) | 91% (TOTAL 1034 stmts, 91 missed) |
| Coverage (whole repo) | 95% |
| Architecture deviations | None |

---

## LOC

| Metric | Count |
|--------|-------|
| Production LOC (`src/kisuke/cli/` + `src/kisuke/application/`) | 1916 |
| Test LOC (`tests/cli/` + `tests/application/`) | 557 |
| Implemented commands | 54 |

---

## Test Inventory

- **CLI end-to-end (`test_cli.py`):** init (+idempotent), status, mission
  create/list/show/archive, project requires mission / create / open, task
  add/list/next/done/move, knowledge add/open, cookbook search/open, decision
  add/list/show, meeting add/today/list, person add/list/show, resource
  add/list/open, resume, review (4 kinds), search, validate, doctor, index
  build/update/clean, sync, plugin lifecycle (+missing remove), config
  get/set (+unknown key)/edit, JSON flag both positions, exit codes
  (not-found=3, bad-uuid=4, missing-args=2), help (top-level + subcommand),
  version, completion.
- **Snapshot (`test_snapshots.py`):** completion bash/zsh, top-level help,
  mission help, task help, version — compared against stored snapshots.
- **Application (`test_app.py`):** `build_entity` ownership/status, `entity_to_dict`
  serialization, `EntityService` CRUD + project registration, `TaskService`
  next/done/move, `PluginService` lifecycle, `ConfigService` get/set,
  `resolve_config` merge, `workspace` init/status/root resolution.

---

## Notes / Design Decisions

- **Application layer added.** The engineering architecture places Application
  between CLI and Domain; the package was empty, so M6 introduced the
  use-case services the CLI delegates to. This follows the documented layering
  rather than redesigning it.
- **Child entities register in their owner project.** `task add` / `knowledge add`
  / `decision add` append their id to the owning project's `tasks` / `knowledge` /
  `decisions` list so that `resume`, `task next`, and validation see consistent
  relationships. This is orchestration only — no Domain rule changed.
- **Review commands aggregate read-only context.** They produce a deterministic
  Markdown report from the Resume engine and stored `Review` entities. They do not
  mutate the repository; the persistent review engine remains a later milestone.
- **`sync`** is implemented as an incremental index update (keeps the index in
  sync with the repository). **`status`** reports per-type entity counts and
  initialization state.
- **`config`** resolves from environment variables (precedence) merged with a JSON
  settings file (`data_dir/settings.json`); `get/set/edit` manage that file.
  No secrets are written.
- **`plugin`** commands manage a local JSON registry under `data_dir`; no plugin
  code is executed (plugins are isolated, M10).

---

## Exit Criteria (per roadmap M6)

- CLI framework: **PASS**
- All documented commands: **PASS**
- JSON + human output: **PASS**
- Exit codes: **PASS**
- Help output: **PASS**
- Snapshot tests: **PASS**
- Ruff: **PASS**
- MyPy (strict): **PASS**
- Pytest: **PASS**

**Result: PASS.** Awaiting approval before starting M7 (Reviews).
