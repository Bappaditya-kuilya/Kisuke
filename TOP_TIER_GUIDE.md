# Making kisuke-mcp Top-Tier

This document outlines what "top-tier" means for this project and how to get there.

## Current State (v0.1.0)

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Functionality** | 8/10 | Core MCP server, 12 tools, 3 resources, 2 prompts, FTS5, migrations, export |
| **Reliability** | 7/10 | Tests pass, race detector clean, but no integration tests, no health endpoint |
| **Observability** | 5/10 | Structured logging (slog), but no metrics, no tracing, no health check |
| **Developer Experience** | 6/10 | Good README, but no generated docs, no SDK examples, no CLI help text polish |
| **Security** | 8/10 | 0600 DB perms, no secrets, but no supply chain verification (sigstore) |
| **Performance** | 8/10 | ~25MB baseline, <100ms query latency, but no benchmarks in CI |
| **Maintainability** | 7/10 | Clean architecture (interface/implementation), but some large files (>600 lines) |

---

## Priority Roadmap

### P0 — Must Have (Next 2-4 weeks)

#### 1. Health Check & Metrics
```go
// Add to internal/mcp/server.go
func (s *Server) HealthCheck() error {
    // Check DB connectivity, MCP connections, Kisuke index reachable
    return s.store.DB().Ping()
}

// Expose via HTTP mode
// GET /healthz -> 200 OK { "status": "healthy", "checks": {...} }
```
- Add `/healthz` endpoint in HTTP mode
- Add Prometheus metrics: `mcp_requests_total`, `mcp_request_duration_seconds`, `db_query_duration_seconds`
- Export via `/metrics` endpoint

#### 2. Integration Tests
```bash
# test/integration_test.go
func TestMCPServer_RealDB(t *testing.T) {
    // Spin up real SQLite, test all 12 tools end-to-end
}
```
- Run against real SQLite (not `:memory:`)
- Test MCP protocol compliance
- Add to CI pipeline

#### 3. Watch Mode for Vault Indexing
```go
// internal/store/watch.go
func (s *sqliteStore) WatchVault(ctx context.Context, vaultPath string) error {
    watcher, _ := fsnotify.NewWatcher()
    watcher.Add(vaultPath)
    for {
        select {
        case event := <-watcher.Events:
            if event.Op&fsnotify.Write == fsnotify.Write {
                s.IndexVaultNote(event.Name, ...)
            }
        case <-ctx.Done():
            return ctx.Err()
        }
    }
}
```
- CLI: `kisuke-mcp watch --vault /path/to/vault`
- Debounce writes (500ms)
- Re-index on create/modify/delete

#### 4. Session Feedback Loop
```sql
-- Already in schema: context_history.user_rating, user_feedback
-- Add MCP tool:
rate_context(session_id, rating: 1-5, feedback: string)
```
- Morning brief shows "Was yesterday's context useful?" 
- Weight forgotten note retrieval by historical ratings

---

### P1 — Should Have (Next 1-2 months)

#### 5. Optional Embedding Search (build tag)
```go
// +build embeddings

// internal/store/embeddings.go
func (s *sqliteStore) SearchVaultNotesSemantic(query string, limit int) ([]VaultLink, error) {
    // Use sentence-transformers via ONNX or CGO
    // Store embeddings in separate table, cosine similarity search
}
```
- Build tag: `go build -tags embeddings`
- Adds ~80MB binary, ~100MB RAM
- Falls back to FTS5 if not built

#### 6. Auto-Link Suggestions
```go
// internal/mcp/suggestions.go
func (s *Server) SuggestLinks(sessionID string) ([]LinkSuggestion, error) {
    // Analyze injected context + session history
    // Find vault notes with high semantic similarity to Kisuke entities
    // Return top 3 with confidence > 0.7
}
```
- MCP prompt: `link_suggestions { session_id }`
- Shows in morning brief: "You worked on SearchEngine — link to 'Search Architecture.md'?"

#### 7. Multi-Vault Support
```go
// Config: VAULT_PATHS="/vault1:/vault2" (colon-separated)
// Index each vault with prefix: "work/", "personal/"
// Search across all, filter by vault in results
```

#### 8. Git-Backed Cross-Machine Sync
```bash
# kisuke-mcp sync init --remote origin
# kisuke-mcp sync push
# kisuke-mcp sync pull
```
- SQLite db + migration history in git
- Conflict resolution: last-write-wins per table, merge context_history
- Encrypt sensitive fields (calendar tokens) with age/rage

---

### P2 — Nice to Have (Later)

#### 9. Generated SDK / Client Libraries
```bash
# Generate from MCP schema
mcp-codegen --input kisuke-mcp --output ./sdks/go
mcp-codegen --input kisuke-mcp --output ./sdks/python
```
- Type-safe clients for Go, Python, TypeScript
- Published to pkg.go.dev, PyPI, npm

#### 10. Visual Dashboard (Web UI)
```bash
kisuke-mcp dashboard --port 8080
```
- View vault links, skill progress, calendar, context history
- Built with HTMX + Tailwind (tiny, no SPA complexity)
- Read-only by default, write via MCP tools

#### 11. Plugin System for MCP Host
```go
// Register custom tool handlers at runtime
s.RegisterTool("my_custom_tool", MyHandler)
// Load from .so plugins (Go plugin) or WASM (extism)
```

#### 12. Benchmark Suite in CI
```yaml
# .github/workflows/benchmark.yml
- name: Run benchmarks
  run: |
    go test -bench=. -benchmem ./internal/store/... > bench.txt
    benchstat -col /old/ /new/ bench.txt
```
- Track query latency, memory alloc, binary size over time
- Fail CI if regression >10%

---

## Anti-Goals (Explicitly NOT Doing)

| Feature | Reason |
|---------|--------|
| Cloud sync / hosted service | Violates "local-first" |
| Electron/Tauri desktop app | Unnecessary binary bloat |
| GraphQL API | MCP is the protocol |
| Plugin marketplace | Supply chain risk |
| Mobile app | Not a mobile use case |
| AI-generated code | Core stays human-written |

---

## Quality Gates

Every PR must pass:
```bash
# Local
go test -race -tags fts5 ./internal/...
go build -tags fts5 ./cmd/kisuke-mcp
golangci-lint run
gosec ./...

# CI (automated)
- Test (race detector)
- Lint (golangci-lint)
- Security (gosec)
- Build matrix (Go 1.23/1.24 × linux/macos)
```

### Before Release (v0.2.0+)
- [ ] All P0 items done
- [ ] Benchmark baseline recorded
- [ ] CHANGELOG.md updated
- [ ] Version tag pushed (`git tag v0.2.0`)
- [ ] GitHub Release with binary artifacts
- [ ] Homebrew formula updated (if applicable)

---

## Architecture Principles (Ponytail Discipline)

1. **Delete before adding** — If a feature has <5 users, remove it
2. **Stdlib first** — No `viper`, `cobra`, `zap` — use `flag`, `slog`, `embed`
3. **One implementation per interface** — No `MockStore` in production code
4. **No config files** — All via env vars or CLI flags
5. **Binary <10MB** — Strip symbols: `go build -ldflags="-s -w"`
6. **Tests in same package** — `_test.go` files, no separate test pkg
7. **Build tags for optional features** — `embeddings`, `webui`, not runtime config

---

## Measuring Success

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Binary size | <10MB | `ls -lh kisuke-mcp` |
| Cold start (stdio) | <200ms | `time kisuke-mcp --version` |
| Query latency (p99) | <50ms | Benchmark `SearchVaultNotes` |
| Memory baseline | <30MB | `ps -o rss= -p $PID` |
| Test coverage | >80% | `go test -cover ./internal/...` |
| CI time | <5min | GitHub Actions duration |
| Vulnerabilities | 0 high/crit | `gosec` + `govulncheck` |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Commit message format (Conventional Commits)
- Branch naming
- PR checklist
- Code review guidelines

---

*This guide evolves. Update it when priorities shift.*