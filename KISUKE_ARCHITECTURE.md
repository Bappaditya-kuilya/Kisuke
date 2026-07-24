# Kisuke Architecture Documentation

*Generated from analysis of the Kisuke codebase (v0.1.0)*

---

## Overview

Kisuke is a **local-first context reconstruction system** written in Python 3.12+. It reconstructs working context from Markdown files organized as a domain-driven knowledge graph.

**Core promise**: "Kisuke does not return notes. Kisuke returns working context."

---

## Architecture (Frozen)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DOMAIN LAYER (Pure Python)                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │  Entities    │ │  IDs         │ │Relationships │ │Lifecycle   │  │
│  │  11 types    │ │  ULID-based  │ │  Bidirectional│ │ Statuses   │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘  │
│  ┌──────────────┐ ┌──────────────┐                                    │
│  │ Validation   │ │ Exceptions   │                                    │
│  │ Schema-based │ │ Domain errors│                                    │
│  └──────────────┘ └──────────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                               │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐   │
│  │ ResumeService   │ │ SearchService   │ │ EntityAppService    │   │
│  │ (context engine)│ │ (hybrid search) │ │ (CRUD operations)   │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                             │
│  ┌──────────────────┐ ┌──────────────────┐ ┌────────────────────┐   │
│  │ FileRepository   │ │ SearchIndex      │ │ ResumeState        │   │
│  │ (Markdown files) │ │ (SQLite FTS)     │ │ (focus tracking)   │   │
│  └──────────────────┘ └──────────────────┘ └────────────────────┘   │
│  ┌──────────────────┐ ┌──────────────────┐ ┌────────────────────┐   │
│  │ Markdown Import  │ │ Git Integration  │ │ Change Detection   │   │
│  │ (Obsidian/Logseq)│ │ (auto-commit)    │ │ (watcher)          │   │
│  └──────────────────┘ └──────────────────┘ └────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Domain Model (11 Entity Types)

| Entity | Purpose | Folder |
|--------|---------|--------|
| **Mission** | High-level goal/intent | `missions/` |
| **Project** | Work unit owned by Mission | `projects/` |
| **Task** | Actionable work item | `tasks/` |
| **Knowledge** | Learned concepts/notes | `knowledge/` |
| **Cookbook** | Reusable patterns/recipes | `cookbook/` |
| **Decision** | Architectural choices | `decisions/` |
| **Meeting** | Meeting records | `meetings/` |
| **Person** | People references | `people/` |
| **Resource** | External links/files | `resources/` |
| **Review** | Periodic retrospectives | `reviews/` |
| **Attachment** | Binary/file references | `attachments/` |

**Relationships** are bidirectional references stored on both entities:
- Project → Mission (owner), Tasks, Knowledge, Decisions, Meetings, Resources, People
- Mission → Reviews
- Knowledge → Resources
- Task → References (Resources)
- Decision → References (Resources)
- Meeting → Projects, People

---

## Storage Model

### Markdown Files (Source of Truth)
- One entity per `.md` file in type-specific folder
- Frontmatter = structured fields (id, type, title, owner, status, tags, relationships)
- Body = free-form Markdown content
- Atomic writes via temp file + `os.replace()`

### SQLite Search Index (Derived, Rebuildable)
```sql
-- entities table (one row per entity)
CREATE TABLE entities (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,        -- entity type enum value
    title TEXT NOT NULL,
    owner TEXT NOT NULL,       -- owner entity id or sentinel
    status TEXT NOT NULL,      -- ACTIVE, ARCHIVED, COMPLETED, etc.
    tags TEXT NOT NULL,        -- space-separated
    body TEXT NOT NULL,        -- full markdown body for FTS
    content_hash TEXT NOT NULL -- sha256 for incremental updates
);

-- tokens table (inverted index)
CREATE TABLE tokens (
    token TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    field TEXT NOT NULL       -- 'title', 'tag', or 'body'
);
CREATE INDEX idx_token ON tokens(token);
```

---

## ResumeService (Context Engine)

The heart of Kisuke. Given a focus mission/project, it:

1. **Loads all entities** from Markdown files
2. **Selects focus mission** (override → active → first)
3. **Selects focus project** (override → active under mission → first)
4. **Traverses 1-hop relationships** from project:
   - Direct: tasks, knowledge, decisions, meetings, resources, people
   - Inverse: meetings referencing project
   - Transitive: resources from knowledge/tasks/decisions
   - People from meetings
4. **Builds ResumeResult** with mission, project, next_action, and all related entities

**Output**: Complete working context for AI/human to resume work.

---

## CLI Commands

```bash
kisuke resume [--project ID] [--mission ID]    # Reconstruct context
kisuke search <query> [--type TYPE]            # Hybrid search
kisuke entity create <type> [fields...]        # Create entity
kisuke entity show <id>                        # Show entity
kisuke entity update <id> [fields...]          # Update entity
kisuke entity delete <id>                      # Delete entity
kisuke index build [--reset]                   # Build search index
kisuke watch                                   # Auto-sync on changes
kisuke import --source <path> --format FMT     # Import from Obsidian/Logseq
kisuke config init                             # Initialize workspace
kisuke focus set --project ID --mission ID     # Set focus
```

---

## Search Engine

**Hybrid BM25 + Vector (optional)**:
- SQLite FTS5 for keyword search (BM25 ranking)
- Optional sentence-transformers for semantic search
- Tokenization: Porter stemmer + lowercase + alnum filtering

**Index fields**: title (weight 3.0), tags (2.0), body (1.0)

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Markdown as source of truth | Human-readable, git-friendly, portable |
| File per entity | Atomic operations, simple diff, no corruption |
| SQLite for search | Zero deps, FTS5 built-in, rebuildable |
| ULID for IDs | Sortable, URL-safe, no coordination |
| 1-hop traversal | Prevents context explosion, O(n) not O(n²) |
| Frontmatter + body | Structured + unstructured in one file |
| Sentinel owners | System entities (USER, ORPHAN) without IDs |
| Plugins never modify core | Stability, testability |

---

## Database Schema for kisuke-mcp Integration

The kisuke-mcp Go bridge needs to read from Kisuke's SQLite search index:

```sql
-- Kisuke's search index (read-only for bridge)
SELECT id, type, title, owner, status, tags, body
FROM entities
WHERE type IN ('project', 'mission', 'knowledge', 'decision', 'task');

-- For relationship traversal, need to parse frontmatter from Markdown files
-- (relationships not stored in SQLite index, only in MD files)
```

---

## Markdown Storage Format

Each entity is stored as a `.md` file with YAML frontmatter + body:

```markdown
---
id: "01ABC..."
type: "project"
title: "My Project"
owner: "01XYZ..."          # mission ULID or sentinel (USER, ORPHAN)
status: "ACTIVE"
priority: "HIGH"
next_action: "01DEF..."
tasks: ["01TASK1...", "01TASK2..."]
knowledge: ["01KNOW1..."]
decisions: ["01DEC1..."]
meetings: ["01MEET1..."]
resources: ["01RES1..."]
people: ["01PER1..."]
tags: ["tag1", "tag2"]
references: ["01REF1..."]
attachments: ["01ATT1..."]
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
---

# Goal
Project description here...

# Description
Additional body content...
```

**Frontmatter rules:**
- Flat key-value (no nesting)
- Scalars: strings (quoted), ints, bools, null
- Lists: YAML array with `- item` syntax
- EntityId lists: `- "01ULID..."`
- Owner: ULID string or sentinel (`USER`, `ORPHAN`)
- Timestamps: ISO8601 strings

**Body sections:** Named sections per entity type (e.g., `## Goal` for Mission, `## Summary` for Decision)

---

## Resume State File

Location: `<repo>/.kisuke/resume_state.json`

```json
{
  "focus_project_id": "01PROJECT...",
  "focus_mission_id": "01MISSION..."
}
```

Updated by `kisuke focus set --project ID --mission ID`.