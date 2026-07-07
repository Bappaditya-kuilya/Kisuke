# Roadmap

> Source: MASTER_SPECIFICATION.md §14

---

# Purpose

This roadmap defines the implementation order of Kisuke.

Features are implemented only after the previous milestone is complete.

Architecture takes priority over speed.

---

# Development Principles

- Documentation First
- One Milestone at a Time
- No Architecture Drift
- Test Before Merge
- Working Software over Feature Count

---

# Milestone Overview

| Milestone | Status | Goal |
|------------|--------|------|
| M0 | Planned | Repository Bootstrap |
| M1 | Planned | Domain Core |
| M2 | Planned | Markdown Storage |
| M3 | Planned | Parser & Validation |
| M4 | Planned | Search Engine |
| M5 | Planned | Resume Engine |
| M6 | Planned | CLI |
| M7 | Planned | Review System |
| M8 | Planned | Integrations |
| M9 | Planned | AI Layer |
| M10 | Planned | Plugin System |
| M11 | Planned | Polish & Release |

---

# M0 — Repository Bootstrap

Goal

Create the engineering foundation.

Deliverables

- Project structure
- Build system
- Logging
- Configuration
- Dependency management
- Test framework

Exit Criteria

- Repository builds
- Tests run
- CI passes

---

# M1 — Domain Core

Goal

Implement every entity defined in the Domain Model.

Deliverables

- Mission
- Project
- Task
- Knowledge
- Cookbook
- Decision
- Meeting
- Person
- Resource
- Review
- Attachment

Exit Criteria

- Domain tests pass
- Ownership rules enforced
- Relationships validated

---

# M2 — Markdown Storage

Goal

Persist all entities in Markdown.

Deliverables

- Markdown parser
- Markdown writer
- Metadata parser
- Validation

Exit Criteria

- Round-trip lossless
- Canonical format preserved

---

# M3 — Parser & Validation

Goal

Guarantee repository integrity.

Deliverables

- Schema validation
- Reference validation
- Ownership validation
- Lifecycle validation

Exit Criteria

- Invalid repositories rejected

---

# M4 — Search Engine

Goal

Fast local search.

Deliverables

- Index builder
- Incremental updates
- Ranking
- Filters

Exit Criteria

- Warm search <500 ms

---

# M5 — Resume Engine

Goal

Core feature of Kisuke.

Deliverables

- Context reconstruction
- Context bundle
- Next Action
- Related entities

Exit Criteria

- Resume flow deterministic
- Context reconstruction complete

---

# M6 — CLI

Goal

Keyboard-first interface.

Deliverables

- Commands
- Help
- JSON output
- Configuration

Exit Criteria

- Every core workflow available from CLI

---

# M7 — Review System

Goal

Periodic system maintenance.

Deliverables

- Morning Review
- Weekly Review
- Monthly Review
- Quarterly Review

Exit Criteria

- Reviews generated correctly

---

# M8 — Integrations

Goal

Connect external tools.

Integrations

- Git
- GitHub
- Obsidian
- VS Code
- Google Calendar

Exit Criteria

- Every integration optional
- Core unaffected by failures

---

# M9 — AI Layer

Goal

Optional AI enhancement.

Deliverables

- Provider abstraction
- Prompt system
- Context summarization
- Classification

Exit Criteria

- Works with multiple providers
- Core works without AI

---

# M10 — Plugin System

Goal

Safe extensibility.

Deliverables

- Plugin API
- Registry
- Loader
- Validation

Exit Criteria

- Plugins isolated
- Core unchanged

---

# M11 — Polish & Release

Goal

Prepare for production.

Deliverables

- Performance optimization
- Documentation review
- Security audit
- Bug fixing
- Packaging

Exit Criteria

- All milestones complete
- Tests passing
- Documentation synchronized
- Release candidate ready

---

# Release Criteria

Kisuke v1 ships only when:

- All milestones complete
- Architecture unchanged
- Tests passing
- Performance targets met
- Documentation complete
- No critical defects remain

---

# Future Roadmap

Out of Scope for v1

- Mobile application
- Web application
- Team collaboration
- Cloud synchronization
- Multi-user support
- Authentication
- Marketplace

Future work requires an RFC and ADR.

---

# Final Principle

Finish one milestone completely before starting the next.

Progress is measured by completed architecture, not completed features.