# M3 Verification Report — Parser & Validation

> Milestone: M3 (Parser & Validation) of the canonical order
> Repository → Domain → Storage → **Parser & Validation** → Search → Resume → CLI → Reviews → Integrations → AI → Plugins → Polish
> Status: Implementation complete, awaiting approval to proceed to M4.

---

## Scope

Implemented the Validator / Parser package in the Infrastructure layer. It scans
the Markdown repository, parses entity files incrementally, validates raw
frontmatter (schema + lifecycle), and validates the parsed collection (ownership,
relationships, duplicate IDs). Results are returned as a deterministic
`ValidationReport`. The validator is read-only: it never modifies repository
contents. Implementation derives from `docs/architecture/04-domain-model.md`
(Ownership Rules, Relationship Model, Cardinality), `docs/architecture/06-data-model.md`
(Universal Entity Schema), and `docs/engineering/12-engineering-architecture.md`
(Storage Architecture).

---

## Files Added

| File | Purpose |
|------|---------|
| `src/kisuke/infrastructure/validation/__init__.py` | Package exports |
| `src/kisuke/infrastructure/validation/report.py` | `ValidationIssue`, `ValidationReport`, `IssueCode`, `IssueSeverity`, text/JSON rendering |
| `src/kisuke/infrastructure/validation/scanner.py` | `RepositoryScanner` — discovers entity `*.md` files per type folder |
| `src/kisuke/infrastructure/validation/parser.py` | `IncrementalParser`, `ParseCache`, `ParseResult` — cached Markdown→entity parsing |
| `src/kisuke/infrastructure/validation/schema.py` | `schema_issues` — Universal Entity Schema validation on raw frontmatter |
| `src/kisuke/infrastructure/validation/validator.py` | `RepositoryValidator` — orchestrates scan/parse/schema/collection validation |
| `tests/infrastructure/validation/__init__.py` | Test package |
| `tests/infrastructure/validation/conftest.py` | Fixtures: valid repo builder + raw frontmatter writers |
| `tests/infrastructure/validation/test_scanner_parser.py` | Scanner discovery + incremental parser |
| `tests/infrastructure/validation/test_schema.py` | Schema validation |
| `tests/infrastructure/validation/test_validator.py` | Repository validator: valid, corrupted, dup-id, orphan, ownership, lifecycle, invalid-ref, read-only, determinism, rendering |
| `tests/infrastructure/validation/test_validator_relationships.py` | Relationship/ownership edge cases |
| `reports/m3-coverage.txt` | Coverage report |
| `htmlcov/` | HTML coverage |

---

## Milestone Scope Coverage

| # | Scope item | Where |
|---|-----------|-------|
| 1 | Repository scanner | `scanner.RepositoryScanner.discover` |
| 2 | Incremental parser | `parser.IncrementalParser` (+ `ParseCache` keyed by mtime+size) |
| 3 | Entity discovery | scanner + parser yield all entities |
| 4 | Reference validation | `validator._check_relationships` (generic `references`) |
| 5 | Ownership validation | `validator._check_ownership` (structure + target) |
| 6 | Lifecycle validation | `validator._lifecycle_issues` (status enum per type) |
| 7 | Schema validation | `schema.schema_issues` (Universal Entity Schema) |
| 8 | Duplicate ID detection | `validator._validate_collection` |
| 9 | Repository consistency validation | `RepositoryValidator.validate` → `ValidationReport.is_valid` |
| 10 | Validation report generation | `report.ValidationReport.render_text` / `render_json` |

---

## Requirements Check

- **Validate the entire repository** — `validate()` scans every type folder and checks every file plus the whole collection.
- **Deterministic results** — issues are sorted by `(code, entity_id, message)` in `ValidationReport.__post_init__`; `test_results_are_deterministic` passes.
- **Detect orphan references** — `ORPHAN_REFERENCE` for missing `references`, relationship targets, attachments, and `next_action`.
- **Detect invalid ownership** — `OWNERSHIP` for sentinel mismatch, missing owner entity, and wrong owner type.
- **Detect duplicate IDs** — `DUPLICATE_ID`.
- **Detect schema violations** — `SCHEMA` for missing/invalid required fields, bad UUID, bad type, bad timestamps, non-list fields.
- **Detect invalid lifecycles** — `LIFECYCLE` for status values not in the per-type enum.
- **Detect broken relationships** — `INVALID_REFERENCE` for disallowed target types, duplicates, and non-Attachment attachments.
- **Validation must not modify repository contents** — `test_validation_is_read_only` confirms byte-identical files before/after.
- **Incremental validation avoids reparsing unchanged files** — `ParseCache` keyed by `(mtime_ns, size)`; `test_incremental_parser_avoids_reparse` confirms `parse_count` does not grow on a second pass.

---

## Verification Results

| Check | Result |
|-------|--------|
| Ruff (`ruff check .`) | All checks passed |
| MyPy (`mypy`, strict) | Success: no issues found in 30 source files |
| Pytest | 138 passed |
| Coverage | 98% (TOTAL 1026 stmts, 25 missed) |
| Architecture deviations | None |

---

## LOC

| Metric | Count |
|--------|-------|
| Production LOC (`src/kisuke/infrastructure/validation/`) | 624 |
| Test LOC (`tests/infrastructure/validation/`) | 407 |

---

## Test Inventory (138 tests)

- **Scanner / Parser (12):** discovery count, unknown-folder isolation, valid parse, unparseable file, malformed owner, incremental cache hit.
- **Schema (7):** valid (no issues), missing field, invalid UUID, invalid type, bad timestamp, non-list field, empty owner.
- **Validator core (11):** valid repo, corrupted (schema), duplicate ID, orphan reference, ownership violation, lifecycle violation, invalid reference type, read-only, determinism, text/JSON rendering.
- **Validator relationships (9):** duplicate typed reference, sentinel-rejected owner, missing owner, duplicate generic reference, attachment orphan, attachment wrong type, next-action orphan, next-action wrong type, malformed-owner parse error.

---

## Notes / Design Decisions

- **Reuses Domain rule tables, does not modify Domain.** Ownership, relationship, and lifecycle rules are imported from `kisuke.domain.relationships` and `kisuke.domain.lifecycle` — the single source of truth — and applied at the repository level with precise per-entity issue attribution (rather than re-parsing the Domain's combined error strings).
- **Layered pipeline.** Each file flows: read frontmatter → `SCHEMA` → `LIFECYCLE` → (construct entity) → collection checks. A malformed file is reported as `SCHEMA` (when the frontmatter is readable but invalid) or `PARSE_ERROR` (when the frontmatter is unreadable or the entity cannot be constructed), never silently dropped.
- **Read-only by construction.** The validator only calls `path.read_text` / `path.stat`; it never writes.
- **Storage behavior unchanged.** Existing `infrastructure/storage` was not modified.

---

## Exit Criteria (per roadmap M3)

- Repository validation tests: **PASS**
- Corrupted repository tests: **PASS**
- Duplicate ID tests: **PASS**
- Broken reference tests: **PASS**
- Ownership violation tests: **PASS**
- Lifecycle violation tests: **PASS**
- Ruff: **PASS**
- MyPy (strict): **PASS**
- Pytest: **PASS**

**Result: PASS.** Awaiting approval before starting M4 (Search).
