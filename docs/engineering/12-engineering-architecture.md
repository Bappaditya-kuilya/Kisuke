# Engineering Architecture

> Source: MASTER_SPECIFICATION.md §13

---

# Purpose

This document defines the software architecture of Kisuke.

It specifies how the system is organized.

It does not define business rules.

---

# Architectural Principles

- Clean Architecture
- Domain Driven Design
- Local-first
- Offline-first
- Provider-independent
- Dependency Inversion
- Composition over Inheritance
- Explicit Dependencies

---

# High-Level Architecture

```text
                User
                  │
                  ▼
         CLI / Future UI
                  │
                  ▼
        Application Services
                  │
                  ▼
          Domain (Core)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Infrastructure      Integrations
        │                   │
        ▼                   ▼
 Storage / Index      Git, AI, Calendar,
                      Obsidian, VS Code
```

---

# Layers

## Presentation

Responsible for:

- CLI
- Future Desktop UI

Never contains business logic.

---

## Application

Responsible for:

- Use cases
- Commands
- Orchestration
- Validation

Coordinates the Domain.

---

## Domain

Responsible for:

- Entities
- Business Rules
- Ownership
- Relationships
- Context Reconstruction

The Domain must not depend on any external library.

---

## Infrastructure

Responsible for:

- Markdown
- SQLite
- File System
- Indexes
- Cache

Implements interfaces defined by the Domain.

---

## Integrations

Responsible for:

- Git
- GitHub
- Obsidian
- Google Calendar
- AI Providers
- VS Code

Never accessed directly by the Domain.

---

# Dependency Rule

Dependencies always point inward.

```text
CLI
 ↓
Application
 ↓
Domain

Infrastructure ─┘

Integrations ───┘
```

The Domain depends on nothing.

---

# Core Modules

```text
core/
├── domain/
├── application/
├── storage/
├── search/
├── resume/
├── review/
├── parser/
└── validation/
```

---

# Infrastructure Modules

```text
infrastructure/
├── markdown/
├── sqlite/
├── filesystem/
├── cache/
└── indexing/
```

---

# Integration Modules

```text
integrations/
├── git/
├── github/
├── obsidian/
├── vscode/
├── calendar/
└── ai/
```

---

# Plugin Modules

```text
plugins/
├── interfaces/
├── registry/
└── loader/
```

Plugins are isolated.

---

# AI Architecture

```text
Domain
   │
   ▼
AI Service
   │
   ▼
Provider Adapter
   │
   ▼
Model
```

Providers never communicate directly with the Domain.

---

# Storage Architecture

```text
Markdown
     │
     ▼
Parser
     │
     ▼
Domain Objects
     │
     ▼
Search Index
```

Markdown remains canonical.

---

# Search Architecture

```text
Markdown
      │
      ▼
Indexer
      │
      ▼
SQLite Index
      │
      ▼
Search Engine
```

Indexes are rebuildable.

---

# Resume Architecture

```text
Project
     │
     ▼
Relationships
     │
     ▼
Current State
     │
     ▼
Next Action
     │
     ▼
Context Bundle
```

Resume is deterministic.

---

# Error Handling

Errors are classified as:

- Validation
- Domain
- Infrastructure
- Integration
- AI

Every error is structured.

---

# Configuration

Configuration is external.

Supported:

- Environment Variables
- Configuration File

No hardcoded secrets.

---

# Performance Targets

CLI Startup

<200 ms

Resume

<2 seconds (warm cache)

Search

<500 ms

Index Update

Incremental only

---

# Testing Strategy

Every layer is tested independently.

| Layer | Test Type |
|--------|-----------|
| Domain | Unit |
| Application | Unit + Integration |
| Infrastructure | Integration |
| Integrations | Mock + Integration |
| CLI | End-to-End |

---

# Extensibility

New capabilities should be added by:

1. New adapter
2. New plugin
3. New integration

Core modifications require architectural review.

---

# Acceptance Criteria

The Engineering Architecture is complete when:

- Dependencies point inward.
- Core has no external dependencies.
- Infrastructure is replaceable.
- Providers are interchangeable.
- Plugins are isolated.
- Markdown remains canonical.
- Architecture satisfies the Constitution.