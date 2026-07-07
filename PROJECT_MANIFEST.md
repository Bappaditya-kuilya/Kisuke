# PROJECT MANIFEST

**Project:** Kisuke

**Status:** Architecture Frozen (v1)

**Document Status:** Canonical

---

# Purpose

Kisuke is a local-first context reconstruction system.

Its purpose is to reduce the time and mental effort required to resume meaningful work by reconstructing working context instead of requiring manual reconstruction.

---

# Core Promise

> Kisuke does not return notes.

> Kisuke returns working context.

---

# Mission

Create a reliable system that allows a person to stop work at any time and later resume it with minimal cognitive overhead.

---

# Scope

Kisuke manages working context.

It does not replace:

- Obsidian
- Git
- GitHub
- Google Calendar
- VS Code
- Existing developer tools

Instead, it integrates with them.

---

# Architectural Principles

- Local-first
- Markdown-first
- Git-native
- Offline-first
- Provider-independent
- Single ownership
- Reference over duplication
- Resume before search
- Integrate before rebuild
- Documentation-first development

---

# Non-Negotiable Rules

## 1. Architecture

Architecture is frozen.

Implementation may not redesign architecture.

---

## 2. Documentation

Documentation is authoritative.

Implementation follows documentation.

---

## 3. Ownership

Every entity has exactly one owner.

Relationships never imply ownership.

---

## 4. History

Git is the sole owner of historical record.

Kisuke never creates a competing history.

---

## 5. AI

AI never owns data.

AI operates on data and returns results.

---

## 6. Storage

Markdown is the source of truth.

Indexes and caches are derived artifacts.

---

## 7. Integrations

Prefer integration over rebuilding existing software.

---

## 8. Simplicity

The core remains small and opinionated.

Complexity belongs in adapters and plugins.

---

# Repository Authority

When conflicts occur:

1. Constitution
2. ADRs
3. Master Specification
4. Engineering Documents
5. Source Code

Code never overrides documentation.

---

# Repository Layout

```
/
├── MASTER_SPECIFICATION.md
├── PROJECT_MANIFEST.md
├── CLAUDE.md
├── IMPLEMENTATION_CONTRACT.md
├── DOCUMENT_INDEX.md
│
├── docs/
├── architecture/
├── adrs/
├── rfcs/
├── templates/
├── src/
├── tests/
└── assets/
```

---

# Development Workflow

```
Idea

↓

Master Specification

↓

Architecture Review

↓

Documentation

↓

Implementation

↓

Tests

↓

Review

↓

Merge
```

Implementation never skips documentation.

---

# Milestones

- M0 — Repository
- M1 — Domain Core
- M2 — Storage
- M3 — CLI
- M4 — Resume Engine
- M5 — Search
- M6 — Reviews
- M7 — Integrations
- M8 — AI
- M9 — Plugins

Each milestone must satisfy its acceptance criteria before the next begins.

---

# Success Criteria

Kisuke is successful when it can:

- Resume any project in under two minutes.
- Preserve working context accurately.
- Operate offline without AI.
- Integrate with existing tools.
- Avoid duplicate information.
- Maintain architectural consistency over time.

---

# Out of Scope

Kisuke is not:

- A note-taking application.
- A project management application.
- A cloud service.
- An autonomous AI agent.
- A replacement for Git.
- A replacement for Obsidian.
- A replacement for Google Calendar.

---

# Definition of Complete

The repository is considered complete when:

- The Master Specification is fully implemented.
- Every implementation traces to documentation.
- All milestones are complete.
- All tests pass.
- No architectural violations remain.