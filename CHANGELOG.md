# Changelog

All notable changes to kisuke-mcp are documented here.

## [0.1.0] - 2026-07-24

### Added
- **Core MCP Server** — 12 tools, 3 resources, 2 prompts over stdio/HTTP
- **Store Interface** — `store.Store` interface with `sqliteStore` implementation (zero import cycles)
- **Schema Migrations** — golang-migrate/v4 with embed.FS, versioned SQL in `internal/store/migrations/`
- **Structured Logging** — `slog` with JSON handler, `KISUKE_DEBUG=1` for debug level
- **Filesystem Hardening** — DB file 0600, parent dir 0700, in-memory test DBs skip chmod
- **Confidence Scoring** — Jaccard similarity on tokenized content for `link_note`, bounded [0.5, 0.95]
- **Export Command** — `kisuke-mcp export --format json|markdown` dumps all data
- **Resume Engine** — Reads `.kisuke/resume_state.json`, falls back to Kisuke search index
- **Context History** — Tracks injected context per session with user rating/feedback
- **Skill Progress** — Streak counting (48hr window), level progression, session totals
- **MCP Host Registry** — `add_mcp`/`list_mcps` store connection metadata (no proxy calls)
- **Google Calendar Sync** — Polls events, tags with project, surfaces in context
- **CI/CD Pipeline** — Test (race detector), lint (golangci-lint), security (gosec), matrix build (Go 1.23/1.24 × linux/mac)
- **Tests** — Store unit tests + Context engine tests with race detector

### Fixed
- `GetUpcomingEvents` time comparison now uses RFC3339 strings (was SQLite `datetime('now')` which failed in tests)
- Removed duplicate migration directories (`/migrations` vs `internal/store/migrations`)
- CI Go version bumped to 1.24 to match `go.mod`

### Security
- Database file permissions restricted to owner-only (0600/0700)
- No secrets in codebase — all via environment variables

---

## [Unreleased]

### Planned (see TOP_TIER_GUIDE.md)
- Watch mode for vault indexing (`fsnotify`)
- Session rating feedback loop
- Auto-link suggestions on context injection
- Health check endpoint for HTTP mode
- Optional embedding-based semantic search (build tag `embeddings`)
- Multi-vault support
- Git-backed cross-machine sync