# kisuke-mcp

[![Go Version](https://img.shields.io/badge/Go-1.24+-00ADD8?logo=go)](https://go.dev/)
[![Build Status](https://github.com/Bappaditya-kuilya/kisuke-mcp/workflows/CI/badge.svg)](https://github.com/Bappaditya-kuilya/kisuke-mcp/actions)
[![Go Report Card](https://goreportcard.com/badge/github.com/Bappaditya-kuilya/kisuke-mcp)](https://goreportcard.com/report/github.com/Bappaditya-kuilya/kisuke-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Binary Size](https://img.shields.io/badge/Binary-~10MB-brightgreen)]()

Personal AI Context Layer — A lightweight Go MCP server that connects your code context (Kisuke) with your knowledge vault (Obsidian) and tools (Calendar, etc.).

**Website:** [kisuke.vercel.app](https://kisuke.vercel.app)

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  opencode / Claude session                                │
│  Auto-injects context at SessionStart                     │
│  Calls tools: search_vault, get_forgotten, get_today      │
└────────────────────────┬─────────────────────────────────┘
                         │ MCP (stdio)
┌────────────────────────▼─────────────────────────────────┐
│                  kisuke-mcp (Go binary ~10MB)              │
│                                                           │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Context     │  │ MCP Client   │  │ Calendar        │  │
│  │ Engine      │  │ (connects to │  │ Poller          │  │
│  │ - forgotten │  │  other MCP   │  │ (Google Cal)    │  │
│  │ - profile   │  │  servers)    │  │                  │  │
│  │ - kisuke    │  └──────────────┘  └─────────────────┘  │
│  └──────┬──────┘                                          │
│         │                                                 │
│  ┌──────▼──────────────────────────────────────────────┐  │
│  │              SQLite (vault_links + profile)          │  │
│  │              FTS5 full-text search                   │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    Kisuke DB            Obsidian vault       Other MCP servers
   (SQLite)            (markdown files)      (calendar, postgres, etc.)
```

## Memory Budget

| Component | RAM |
|-----------|-----|
| Go binary | ~10 MB |
| Runtime (goroutines, SQLite pool) | ~10 MB |
| SQLite cache | ~5 MB |
| FTS5 index | ~5 MB |
| MCP client connections | ~2 MB/server |
| **Total baseline** | **~30-35 MB** |
| Embedding model (optional, v2) | ~80-200 MB |

**Peak total: ~105 MB** (well under 200 MB cap)

## Features

### 1. Forgotten Note Retrieval
When you start a coding session, kisuke-mcp finds notes you wrote but forgot about:
- Linked notes (explicit `vault_links`)
- Inferred notes (semantic search via FTS5)
- Returns top 5 with confidence scores and reason

### 2. Project Context Injection
Auto-injects into every opencode session:
- Current project/mission from Kisuke
- Today's calendar events (with project tags)
- Your developer profile (goals, stack, build style)
- Skill progress tracking

### 3. MCP Host Capability
Connect to ANY MCP server without manual wiring:
```bash
# One-time setup
kisuke-mcp add-mcp postgres "npx @modelcontextprotocol/server-postgres"
kisuke-mcp add-mcp calendar "npx @modelcontextprotocol/server-google-calendar"

# Now use from any session
# opencode will call through kisuke-mcp seamlessly
```

### 4. Skill Progress Tracking
Built-in tracking for your learning goals:
- Docker, PostgreSQL, DSA, System Design
- Streak counting, level progression
- Integrated into morning briefing

## Quick Start

```bash
# Build
go build -tags fts5 -o kisuke-mcp ./cmd/kisuke-mcp

# Initialize (one-time)
kisuke-mcp init

# Run (stdio for opencode)
kisuke-mcp

# Or HTTP for other clients
kisuke-mcp -http :8080
```

### opencode Integration

Add to `~/.config/opencode/mcp.json`:
```json
{
  "mcpServers": {
    "kisuke": {
      "command": "/path/to/kisuke-mcp"
    }
  }
}
```

opencode will auto-connect and inject context at every session start.

## MCP Tools Exposed

| Tool | Description |
|------|-------------|
| `get_context` | Full injected context (project, forgotten notes, events, profile, skills) |
| `search_vault` | Search Obsidian vault with FTS5 |
| `link_note` | Create vault_links entry |
| `unlink_note` | Remove vault_links entry |
| `get_forgotten` | Get forgotten notes for a project |
| `get_profile` | Get developer profile |
| `update_profile` | Update profile key/value |
| `get_skills` | Get skill progress |
| `practice_skill` | Log a practice session |
| `add_mcp` | Register an MCP server |
| `list_mcps` | List registered MCP servers |
| `get_upcoming` | Get upcoming calendar events |

## MCP Resources

| URI | Description |
|-----|-------------|
| `kisuke://context/{session_id}` | Full context as JSON |
| `kisuke://vault/search/{query}` | Vault search results |
| `kisuke://profile` | Developer profile |

## MCP Prompts

| Prompt | Description |
|--------|-------------|
| `morning_brief` | Daily briefing with context, schedule, forgotten notes, skills |
| `project_context` | Full project context for coding session |

## Database Schema

```sql
-- Links between vault notes and Kisuke entities
CREATE TABLE vault_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vault_note_path TEXT NOT NULL,
    vault_note_title TEXT NOT NULL,
    kisuke_entity_type TEXT NOT NULL,
    kisuke_entity_id TEXT NOT NULL,
    link_type TEXT DEFAULT 'reference',
    confidence REAL DEFAULT 0.8,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vault_note_path, kisuke_entity_type, kisuke_entity_id)
);

-- FTS5 full-text search over vault notes
CREATE VIRTUAL TABLE notes_fts USING fts5(path, title, content);

-- Your identity and preferences
CREATE TABLE developer_profile (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- What was injected, was it useful?
CREATE TABLE context_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    injected_context TEXT NOT NULL,
    user_rating INTEGER,
    user_feedback TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Learning progress
CREATE TABLE skill_progress (
    skill_name TEXT PRIMARY KEY,
    current_level INTEGER DEFAULT 0,
    target_level INTEGER DEFAULT 5,
    last_practiced DATETIME,
    streak_days INTEGER DEFAULT 0,
    total_sessions INTEGER DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Registered MCP servers
CREATE TABLE mcp_connections (
    name TEXT PRIMARY KEY,
    command TEXT NOT NULL,
    args TEXT DEFAULT '[]',
    env TEXT DEFAULT '{}',
    enabled BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Google Calendar events
CREATE TABLE calendar_events (
    id TEXT PRIMARY KEY,
    summary TEXT NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    calendar_id TEXT NOT NULL,
    project_tag TEXT,
    synced_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Default Profile

On first run, these are set (editable via `update_profile`):
```json
{
  "name": "Bappaditya Kuilya",
  "role": "AI Engineer (aspiring)",
  "goal": "Become elite engineer, master Docker, PostgreSQL, DSA, build resume projects",
  "build_style": "Clean architecture, test-driven, well-documented, minimal deps",
  "preferred_stack": "Go, Python, SQLite, Docker, PostgreSQL",
  "learning_focus": "Docker, PostgreSQL, DSA, System Design, AI/ML"
}
```

## Development

```bash
# Run tests (with race detector)
go test -tags fts5 -race ./internal/...

# Build
go build -tags fts5 -o kisuke-mcp ./cmd/kisuke-mcp

# Run with custom paths
VAULT_PATH=/path/to/vault KISUKE_DB=/path/to/kisuke.db ./kisuke-mcp

# Index vault notes (run periodically)
./kisuke-mcp index-vault

# Export all data (JSON or Markdown)
./kisuke-mcp export --format json
./kisuke-mcp export --format markdown
```

## Project Structure

```
kisuke-mcp/
├── .github/workflows/ci.yml      # CI/CD pipeline
├── cmd/
│   └── kisuke-mcp/
│       └── main.go               # Entry point (subcommands: init, export, serve)
├── internal/
│   ├── context/
│   │   ├── engine.go             # Context engine - determines relevance
│   │   ├── engine_test.go        # Context engine tests
│   │   └── types.go              # Shared types
│   ├── mcp/
│   │   └── server.go             # MCP server with all tools/resources/prompts
│   ├── store/
│   │   ├── store.go              # SQLite operations (golang-migrate)
│   │   ├── store_test.go         # Store unit tests
│   │   ├── types.go              # Store interface + types
│   │   └── migrations/           # Embedded SQL migrations
│   ├── calendar/
│   │   └── calendar.go           # Google Calendar integration
│   └── kisuke/
│       └── resume.go             # Kisuke resume engine client
├── CHANGELOG.md                  # Release history
├── TOP_TIER_GUIDE.md             # Roadmap to top-tier quality
├── go.mod
├── go.sum
└── README.md
```

## Philosophy

> **Storage is solved. Retrieval is the problem.**

You have notes everywhere (Notion, Google Docs, Obsidian). The issue isn't storing them — it's **surfacing the right one at the right time**.

kisuke-mcp doesn't add another note-taking app. It connects what you already have:
- **Kisuke** knows what you're building (code context)
- **Obsidian** holds what you've learned (knowledge)
- **Calendar** knows when things are due (time)
- **kisuke-mcp** connects them so your AI assistant starts every session already knowing *you*

## Roadmap

See [TOP_TIER_GUIDE.md](TOP_TIER_GUIDE.md) for detailed roadmap and quality gates.

- [x] v0.1: Core MCP server, vault_links, FTS5 search, profile, skills, migrations, export, structured logging
- [ ] v0.2: Health endpoint, metrics, watch mode, session feedback, integration tests
- [ ] v0.3: Optional embedding-based semantic search (build tag `embeddings`)
- [ ] v0.4: Auto-link suggestions from session analysis
- [ ] v0.5: Cross-machine sync via git

## License

MIT — Your data, your machine, your rules.