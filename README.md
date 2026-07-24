# context-mcp

[![Go Version](https://img.shields.io/badge/Go-1.24+-00ADD8?logo=go)](https://go.dev/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/kisuke/kisuke-mcp/ci.yml?branch=main)](https://github.com/kisuke/kisuke-mcp/actions)
[![Go Report Card](https://goreportcard.com/badge/github.com/kisuke/kisuke-mcp)](https://goreportcard.com/report/github.com/kisuke/kisuke-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Binary Size](https://img.shields.io/badge/Binary-~10MB-brightgreen)]()

**context-mcp** — A minimal, generic MCP server for personal context injection. Works with any AI assistant (opencode, Claude Code, Codex, etc.).

No Kisuke dependency. No vendor lock-in. Just your notes + SQLite + MCP protocol.

---

## Quick Start

```bash
# Build
go build -tags fts5 -o context-mcp ./cmd/kisuke-mcp

# Initialize (one-time)
context-mcp init

# Run (stdio for MCP clients)
context-mcp

# Or HTTP for other clients
context-mcp -http :8080
```

### opencode / Claude Code / Codex Integration

Add to your MCP config:

```json
{
  "mcpServers": {
    "context": {
      "command": "/path/to/context-mcp",
      "env": {
        "VAULT_PATH": "/path/to/your/notes"
      }
    }
  }
}
```

That's it. Every session starts with your context already loaded.

---

## What It Does

| Feature | Description |
|---------|-------------|
| **search_notes** | FTS5 full-text search over your markdown vault |
| **link_note** | Connect notes to projects (bidirectional) |
| **get_context** | Inject project + relevant notes + profile into session |
| **get_profile** / **update_profile** | Persistent key-value profile (goals, stack, preferences) |
| **add_mcp** / **list_mcps** | Registry for other MCP servers (Postgres, Calendar, etc.) |
| **index_vault** | Scan and index all `.md` files |
| **morning_brief** / **project_context** | Prompt templates for session startup |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AI Assistant (opencode, Claude Code, Codex, etc.)         │
│  Auto-injects context via MCP tools                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ MCP (stdio)
┌──────────────────────────▼──────────────────────────────────┐
│  context-mcp (Go binary ~10MB)                              │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │ SQLite + FTS5   │  │ MCP Registry                    │  │
│  │ - vault_links   │  │ Connect to other MCP servers    │  │
│  │ - notes_fts     │  │ (Postgres, Calendar, GitHub...) │  │
│  │ - profile       │  └─────────────────────────────────┘  │
│  │ - skills        │                                       │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    Your Notes Vault
                   (markdown files)
```

- **Zero config**: All via env vars or CLI flags
- **Portable**: Single binary, SQLite file, notes folder
- **Extensible**: Register any MCP server, call through context-mcp

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_notes` | Full-text search over vault (FTS5) |
| `link_note` | Link note → project with confidence |
| `unlink_note` | Remove link |
| `index_vault` | Scan & index all `.md` files |
| `get_context` | Session injection: project, notes, profile |
| `get_profile` / `update_profile` | Key-value profile store |
| `add_mcp` / `list_mcps` | Register external MCP servers |

## MCP Resources

| URI | Description |
|-----|-------------|
| `context://session/{id}` | Full injected context as JSON |
| `vault://search/{query}` | Search results |
| `context://profile` | Developer profile |

## MCP Prompts

| Prompt | Description |
|--------|-------------|
| `morning_brief` | Daily briefing with project, notes, skills |
| `project_context` | Full context for coding session |

---

## Configuration

| Env Var | Description | Default |
|---------|-------------|---------|
| `VAULT_PATH` | Path to markdown notes folder | (required for search/index) |
| `CONTEXT_MCP_DB` | SQLite database path | `./context-mcp.db` |
| `CONTEXT_DEBUG` | Enable debug logging | `false` |

---

## Development

```bash
# Run tests
go test -tags fts5 -race ./internal/...

# Build
go build -tags fts5 -o context-mcp ./cmd/kisuke-mcp

# Lint
golangci-lint run
```

### Project Structure

```
context-mcp/
├── cmd/kisuke-mcp/main.go      # Entry point (subcommands: init, export, serve)
├── internal/
│   ├── mcp/server.go           # MCP tools, resources, prompts
│   └── store/                  # SQLite + FTS5 storage
│       ├── store.go            # Implementation
│       ├── types.go            # Store interface
│       └── migrations/         # golang-migrate SQL files
├── go.mod
└── README.md
```

---

## Philosophy

> **Storage is solved. Retrieval is the problem.**

You have notes everywhere. The issue isn't storing them — it's **surfacing the right one at the right time**.

context-mcp doesn't add another note-taking app. It connects what you already have:
- **Your notes** (markdown, any structure)
- **Your profile** (goals, stack, preferences)
- **External tools** (via MCP registry)
- **Your AI assistant** (gets context automatically)

---

## License

MIT — Your data, your machine, your rules.