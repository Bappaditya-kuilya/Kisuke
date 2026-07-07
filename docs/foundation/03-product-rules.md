# Product Rules

> Source: MASTER_SPECIFICATION.md §4

---

# Purpose

This document defines the behavioral rules that every part of Kisuke must follow.

These rules apply to:

- Core
- CLI
- AI
- Integrations
- Plugins
- Future extensions

---

# Rule 1 — Single Ownership

Every entity has exactly one owner.

Ownership is explicit.

Ownership is never inferred.

---

# Rule 2 — References Over Duplication

Information is stored once.

Relationships are expressed through references.

Duplicating information to simplify implementation is prohibited.

---

# Rule 3 — Resume Before Search

The primary workflow is:

```
Resume

↓

Understand

↓

Act
```

Search supports this workflow.

Search never replaces it.

---

# Rule 4 — Context Over Notes

Kisuke reconstructs:

- Goal
- Current state
- Decisions
- Next action
- Related knowledge
- Related resources

It does not simply display notes.

---

# Rule 5 — Human Remains in Control

Kisuke recommends.

The user decides.

Kisuke never performs autonomous actions without explicit approval.

---

# Rule 6 — Integrate Before Rebuild

If an existing tool already performs a function well:

Integrate with it.

Do not recreate it.

Examples:

- Git
- Obsidian
- Google Calendar
- GitHub
- VS Code

---

# Rule 7 — AI Is Optional

Every core workflow must function without AI.

AI enhances workflows.

AI never becomes a dependency for core functionality.

---

# Rule 8 — Markdown Is Canonical

Markdown is the authoritative data format.

Everything else is derived.

Examples:

- Search indexes
- SQLite
- Embeddings
- AI summaries
- Caches

All can be rebuilt.

---

# Rule 9 — Git Owns History

History belongs to Git.

Kisuke records current state, not version history.

---

# Rule 10 — Capture First

Every new piece of information follows:

```
Capture

↓

Classify

↓

Reference

↓

Review
```

Organization never blocks capture.

---

# Rule 11 — One Next Action

Each active project may have exactly one current Next Action.

It must represent the highest-priority executable task.

---

# Rule 12 — Decisions Must Be Recorded

Important decisions should include:

- Decision
- Reason
- Alternatives
- Date
- Related project

This prevents repeated decision-making.

---

# Rule 13 — Evergreen Knowledge Belongs in Cookbook

Reusable knowledge belongs in Cookbook.

Project-specific knowledge belongs to the Project.

---

# Rule 14 — Reviews Maintain the System

Reviews exist to prevent entropy.

Supported review types:

- Morning
- Weekly
- Monthly
- Quarterly

---

# Rule 15 — Plugins Respect the Core

Plugins may:

- Read
- Extend
- Suggest

Plugins may not:

- Change ownership
- Modify architecture
- Bypass validation

---

# Rule 16 — Simplicity Wins

When multiple designs satisfy the same requirement:

Choose the simplest one that preserves the architecture.

---

# Validation Checklist

Every feature must satisfy:

- Single ownership
- No duplicated data
- Markdown remains canonical
- Offline core preserved
- Resume workflow improved
- AI optional
- Architecture unchanged

If any answer is **No**, the feature is rejected.