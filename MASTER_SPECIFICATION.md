# Kisuke Master Specification

> **Status:** Draft v1
> **Architecture:** Frozen
> **Source of Truth:** This document

---

# 1. Vision

TODO

# 2. Product Definition

TODO

# 3. Constitution

TODO

# 4. Core Principles

TODO

# 5. Domain Model

TODO
# 5. Domain Model

## Purpose

The Domain Model defines the canonical entities of Kisuke and the relationships between them.

Every other document depends on this model.

---

## Core Entities

### Mission

Represents a long-term objective that guides priorities.

Owner: Kisuke Core

---

### Project

A temporary endeavor with a defined beginning and end undertaken to achieve a unique outcome.

Owner: Mission

---

### Task

A unit of work belonging to exactly one project.

One active task may be designated as the Next Action.

Owner: Project

---

### Knowledge

Persistent information created or collected to support execution.

Owner: Project

---

### Cookbook

Evergreen reusable knowledge independent of a single project.

Owner: Kisuke Core

---

### Decision

A recorded architectural, technical, or operational decision.

Owner: Project

---

### Meeting

A time-bounded discussion that may reference projects, tasks, people, resources and decisions.

Owner: Independent

---

### Person

Represents an individual involved in work.

Owner: Independent

---

### Resource

Represents an external source.

Examples:

- Documentation
- GitHub Repository
- PDF
- Website
- Video
- Dataset

Owner: Independent

---

### Review

Represents a structured evaluation of work.

Types:

- Morning
- Weekly
- Monthly
- Quarterly

Owner: Mission

---

### Attachment

Binary assets.

Examples:

- Images
- PDFs
- Files

Owner: Parent Entity

---

# Relationships

Mission

↓

Projects

Project

↓

Tasks

↓

Knowledge

↓

Decisions

↓

Resources

↓

Meetings

↓

People

Meeting

↓

Projects

↓

Tasks

↓

Decisions

↓

People

↓

Resources

Knowledge

↓

Resources

↓

Projects

Decision

↓

Projects

↓

Resources

↓

Meetings

Cookbook

↓

Knowledge

↓

Resources

Review

↓

Mission

↓

Projects

↓

Tasks

---

# Ownership Rules

Every entity has exactly one owner.

Relationships never imply ownership.

Ownership never changes implicitly.

---

# Invariants

- One owner per entity.
- References instead of duplication.
- No circular ownership.
- AI owns nothing.
- IDs are globally unique.
- Relationships are directional.
- Markdown remains the source of truth.

---

# Entity Lifecycle

Mission

Planning

↓

Active

↓

Completed

↓

Archived

Project

Planning

↓

Active

↓

Blocked

↓

Paused

↓

Completed

↓

Archived

Task

Todo

↓

In Progress

↓

Done

↓

Archived

Knowledge

Draft

↓

Active

↓

Deprecated

↓

Archived

Decision

Proposed

↓

Accepted

↓

Superseded

↓

Archived

Meeting

Scheduled

↓

Completed

↓

Archived

Review

Planned

↓

Completed

↓

Archived

# 6. Information Architecture

TODO

# 7. Data Model

TODO

# 8. User Flows

TODO

# 9. CLI Specification

TODO

# 10. Integrations

TODO

# 11. AI Abstraction

TODO

# 12. Security

TODO

# 13. Engineering Architecture

TODO

# 14. Roadmap

TODO

# 15. Implementation Plan

TODO

# 16. Coding Guidelines

TODO

# 17. Testing Strategy

TODO

# 18. ADR Index

TODO

# 19. Architecture Audit

TODO