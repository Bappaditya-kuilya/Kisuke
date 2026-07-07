# Information Architecture

> Source: MASTER_SPECIFICATION.md §6

---

# Purpose

This document defines how information is organized inside Kisuke.

It does **not** define storage.

It defines logical organization only.

---

# Design Goals

The information architecture must:

- Minimize retrieval time.
- Minimize cognitive load.
- Avoid duplicated information.
- Preserve ownership.
- Support fast context reconstruction.
- Scale to years of accumulated knowledge.

---

# Information Hierarchy

```text
Mission
│
├── Projects
│   ├── Tasks
│   ├── Knowledge
│   ├── Decisions
│   ├── Meetings
│   └── Resources
│
├── Reviews
│
└── Cookbook
```

---

# Information Layers

Kisuke separates information into four layers.

## Layer 1 — Mission

Answers:

> Why am I doing this?

Contains:

- Long-term objectives
- Direction
- Success criteria

---

## Layer 2 — Project

Answers:

> What am I building?

Contains:

- Tasks
- Decisions
- Knowledge
- Meetings
- Resources

---

## Layer 3 — Execution

Answers:

> What should I do now?

Contains:

- Next Action
- Active Task
- Current State
- Active Context

---

## Layer 4 — Knowledge

Answers:

> What have I learned?

Contains:

- Cookbook
- Knowledge
- References
- External Resources

---

# Information Flow

```text
Capture

↓

Classify

↓

Link

↓

Review

↓

Resume
```

---

# Navigation Principles

Every entity must be reachable in three ways.

## 1. Ownership

Example

Mission

↓

Project

↓

Task

---

## 2. Relationships

Example

Task

↓

Decision

↓

Meeting

↓

Resource

---

## 3. Search

Keyword

↓

Entity

↓

Context

Search is always the final fallback.

---

# Context Stack

When opening a Project Kisuke reconstructs:

Mission

↓

Project

↓

Current State

↓

Next Action

↓

Related Tasks

↓

Recent Decisions

↓

Relevant Knowledge

↓

Recent Meetings

↓

Resources

This ordered reconstruction is called the Context Stack.

---

# Navigation Rules

Users should never manually traverse large folder trees.

Navigation is entity-based rather than file-based.

Information should always be discoverable from relationships instead of physical location.

---

# Information Categories

Every piece of information belongs to exactly one category.

| Category | Owner |
|----------|-------|
| Mission | Kisuke Core |
| Project | Mission |
| Task | Project |
| Knowledge | Project |
| Cookbook | Kisuke Core |
| Decision | Project |
| Meeting | Independent |
| Person | Independent |
| Resource | Independent |
| Review | Mission |
| Attachment | Parent Entity |

---

# Classification Rules

Every new entity must answer:

- Who owns me?
- What do I belong to?
- What do I reference?
- Why do I exist?
- When was I created?

---

# Context Reconstruction Model

Context reconstruction is Kisuke's primary capability.

The reconstruction pipeline is deterministic.

```text
Entity
    ↓
Relationships
    ↓
Metadata
    ↓
Current State
    ↓
Next Action
    ↓
Related Context
```

The user should understand **what they were doing** before deciding **what to do next**.

---

# Resume Order

When resuming a Project, Kisuke reconstructs information in this order.

1. Mission
2. Project
3. Project Status
4. Current State
5. Next Action
6. Active Tasks
7. Recent Decisions
8. Relevant Knowledge
9. Related Meetings
10. Related Resources
11. Attachments

The order is fixed.

---

# Context Window

A context window contains only information necessary to continue work.

Included:

- Current Project
- Active Tasks
- Next Action
- Recent Decisions
- Relevant Knowledge
- Required Resources
- Recent Meetings

Excluded:

- Completed Projects
- Archived Tasks
- Unrelated Cookbook entries
- Unrelated Meetings

---

# Information Freshness

Priority is determined by:

1. Explicit pinning
2. Active state
3. Recent modification
4. Relationship strength

Age alone never determines importance.

---

# Context Boundaries

Mission boundaries isolate strategic context.

Project boundaries isolate execution context.

Cookbook boundaries isolate evergreen knowledge.

Reviews span multiple Projects.

Meetings remain independent and reference Projects.

---

# Search Strategy

Search is a supporting capability.

Search order:

```text
Current Context
    ↓
Current Project
    ↓
Mission
    ↓
Cookbook
    ↓
Entire Repository
```

Global search is always the final step.

---

# Relationship Traversal

Traversal follows explicit references only.

Traversal never infers missing links.

Traversal never creates temporary ownership.

Maximum traversal depth is implementation-defined.

---

# Information Density

Every screen should answer:

- Where am I?
- Why am I here?
- What is the current state?
- What should I do next?
- What decisions already exist?

Everything else is secondary.

---

# Cross References

Entities may reference one another.

Allowed examples:

Project → Task

Task → Meeting

Knowledge → Resource

Decision → Resource

Review → Project

References never duplicate information.

---

# Archival Rules

Archived entities:

- Remain searchable.
- Preserve relationships.
- Cannot become active without restoration.
- Never lose historical references.

Deletion is exceptional.

Archiving is the default.

---

# Information Quality Rules

Information should be:

- Atomic
- Explicit
- Traceable
- Reusable
- Linked
- Minimal

Avoid:

- Duplication
- Ambiguity
- Hidden assumptions
- Orphaned entities

---

# Acceptance Criteria

The Information Architecture is complete when:

- Every entity has a clear place.
- Navigation is deterministic.
- Resume flow is defined.
- Search complements, not replaces, resume.
- Ownership remains intact.
- No duplicated information exists.
- Context reconstruction is predictable.

---

# Final Principle

Information exists to reduce cognitive load.

Every structural decision should make resuming work easier than reconstructing it manually.

