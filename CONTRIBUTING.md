# Contributing to kisuke-mcp

Thank you for considering a contribution! This project follows a few simple conventions.

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

<body>

<footer>
```

**Types:**
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation only
- `refactor` — code change that neither fixes a bug nor adds a feature
- `test` — adding or updating tests
- `ci` — CI/CD changes
- `chore` — maintenance (deps, build, etc.)

**Examples:**
```
feat(store): add migration support with golang-migrate
fix(mcp): handle nil confidence in link_note
docs(readme): update architecture diagram
```

## Branch Naming

```
<type>/<short-description>
```

Examples: `feat/watch-mode`, `fix/migration-panic`, `docs/architecture-update`

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] `go test -race -tags fts5 ./internal/...` passes
- [ ] `golangci-lint run` passes
- [ ] `gosec ./...` passes
- [ ] `go build -tags fts5 ./cmd/kisuke-mcp` succeeds
- [ ] New code has tests (if applicable)
- [ ] CHANGELOG.md updated (for user-facing changes)
- [ ] Commit messages follow Conventional Commits

## Code Style

- **No external config libraries** — use `flag` and `os.Getenv`
- **No external logging** — use `log/slog`
- **Interfaces in `types.go`** — implementation in `store.go`
- **Tests in `_test.go`** — same package, no separate test package
- **Build tags for optional features** — `embeddings`, `webui`
- **Binary stripped** — `go build -ldflags="-s -w"`

## Adding a New MCP Tool

1. Define request/response types in `internal/mcp/types.go` (if needed)
2. Add handler method to `Server` in `internal/mcp/server.go`
3. Register in `registerTools()` 
4. Add integration test in `internal/mcp/server_test.go`
5. Update README.md tool table

## Adding a Database Migration

1. Create `internal/store/migrations/00000X_description.up.sql`
2. Create `internal/store/migrations/00000X_description.down.sql`
3. Test: `go test -tags fts5 ./internal/store/...`
4. Migration runs automatically on `NewStore()` via golang-migrate

## Reporting Issues

- Use the GitHub issue template
- Include Go version (`go version`), OS, and steps to reproduce
- For bugs: include logs with `KISUKE_DEBUG=1`

## Code Review

- All PRs require at least one approval
- Reviewers: check for ponytail violations (unnecessary abstractions, stdlib alternatives)
- `golangci-lint` and `gosec` must pass in CI

## Questions?

Open a GitHub Discussion or issue.