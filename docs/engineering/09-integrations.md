# Integrations

> Source: MASTER_SPECIFICATION.md §10

---

# Purpose

This document defines how Kisuke integrates with external systems.

Kisuke integrates.

It does not replace.

---

# Integration Principles

- Local-first
- Read before write
- Explicit user approval
- Loose coupling
- Provider-independent
- Graceful degradation

---

# Categories

- Development
- Knowledge
- Calendar
- AI
- Storage
- Search
- Automation

---

# Development

## Git

Purpose

Version history.

Capabilities

- Repository detection
- Current branch
- Commit metadata
- Recent commits
- Repository status

Git remains the source of truth.

---

## GitHub

Purpose

Repository metadata.

Capabilities

- Issues
- Pull Requests
- Releases
- Repository links

Optional.

---

## VS Code

Purpose

Resume development context.

Capabilities

- Open workspace
- Open file
- Restore session
- Launch project

VS Code owns the editor.

---

# Knowledge

## Obsidian

Purpose

Knowledge storage.

Capabilities

- Read notes
- Create notes
- Link entities
- Open vault

Obsidian remains the note editor.

---

## Markdown

Purpose

Canonical storage.

Capabilities

- Read
- Write
- Parse
- Validate

Markdown is the source of truth.

---

# Calendar

## Google Calendar

Purpose

Meeting synchronization.

Capabilities

- Read events
- Create events
- Update events
- Reminder support

Optional.

Offline operation remains available.

---

# AI

Supported Providers

- OpenAI
- Anthropic
- Google
- Ollama
- OpenRouter
- Any OpenAI-compatible API

Requirements

- Provider abstraction
- API-key based
- Optional
- Replaceable

No provider-specific logic inside Core.

---

# Search

Supported

- Local Index
- Markdown
- File System

Optional

- Vector Search

Search index is rebuildable.

---

# Storage

Primary

- Markdown

Derived

- SQLite
- Cache
- Search Index

Never treat derived storage as canonical.

---

# Automation

Supported

- CLI
- Shell Scripts
- Cron
- Git Hooks

Automation must never bypass validation.

---

# Plugin Architecture

Plugins may integrate with:

- Git
- GitHub
- VS Code
- Obsidian
- Calendar
- AI Providers

Plugins communicate through public interfaces only.

---

# Integration Rules

Integrations may:

- Read
- Import
- Export
- Synchronize
- Open

Integrations may not:

- Own data
- Change ownership
- Modify architecture
- Bypass validation

---

# Failure Handling

If an integration fails:

- Continue core functionality.
- Display meaningful error.
- Never corrupt Markdown.
- Never lose user data.

---

# Security

- Least privilege
- Explicit permissions
- Secrets via environment variables
- No hidden telemetry
- No automatic cloud upload

---

# Acceptance Criteria

- Core works without integrations.
- Every integration is optional.
- Providers are replaceable.
- Markdown remains canonical.
- No integration owns Kisuke data.