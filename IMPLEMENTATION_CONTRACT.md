# IMPLEMENTATION CONTRACT

> This document governs how Kisuke is implemented.

---

# Purpose

Implementation follows architecture.

Architecture never follows implementation.

Every engineering decision must preserve the architecture defined in the Master Specification.

---

# Source of Truth

The canonical authority order is defined once, in docs/foundation/01-constitution.md, § Authority. It is not restated here to avoid drift.

When conflicts exist, the higher document wins.

---

# Development Process

```
Idea
    ↓
Specification
    ↓
Architecture Review
    ↓
Implementation
    ↓
Tests
    ↓
Review
    ↓
Merge
```

Implementation never skips a stage.

---

# Responsibilities

## Architect

Responsible for:

- Product decisions
- Domain model
- Relationships
- Workflows
- Rules
- Architecture

---

## Engineer

Responsible for:

- Implementation
- Tests
- Performance
- Refactoring within architecture
- Bug fixes

---

# Forbidden Actions

Never:

- Redesign architecture
- Invent entities
- Change ownership
- Introduce circular dependencies
- Modify the Constitution
- Implement undocumented behavior
- Skip tests
- Skip reviews

---

# Architecture Changes

Architecture may change only through:

RFC

↓

Review

↓

ADR

↓

Master Specification Update

↓

Implementation

Implementation is always the last step.

---

# Milestone Rules

Only one milestone may be active.

Before starting the next milestone:

- Current milestone completed
- Acceptance criteria satisfied
- Tests passing
- Documentation updated

---

# Coding Rules

Every change must:

- Solve one problem
- Remain backwards compatible unless documented
- Preserve existing behavior
- Keep modules cohesive
- Keep dependencies minimal

---

# Testing Rules

Every feature requires:

- Unit tests
- Integration tests (when applicable)
- Acceptance verification

Bug fixes require regression tests.

---

# Documentation Rules

Every implementation must map back to:

- Requirement
- Section
- Milestone

Undocumented code is not accepted.

---

# Performance Rules

Search

- Warm index <500 ms

CLI

- Startup <200 ms

Resume

- Working context reconstructed with minimal manual effort

Index

- Incremental only

---

# Dependency Policy

A dependency is accepted only if it:

- Solves a real problem
- Is actively maintained
- Can be replaced
- Does not violate architecture

Otherwise reject it.

---

# Error Handling

Recoverable

- Return structured errors.

Fatal

- Fail immediately.

Never silently continue.

---

# Security Rules

- Secrets never committed.
- Environment variables only.
- Least privilege.
- Validate external input.
- No hidden telemetry.

---

# AI Rules

AI is optional.

Core functionality must work without AI.

AI:

May

- Explain
- Summarize
- Search
- Classify
- Resume

May not

- Own data
- Change source documents automatically
- Become the source of truth

---

# Plugin Rules

Plugins:

May

- Read data
- Generate derived artifacts
- Request changes

May not

- Mutate core directly
- Change ownership
- Bypass validation
- Override architecture

---

# Review Checklist

Before merging verify:

- Architecture unchanged
- Documentation updated
- Tests passing
- No duplicated logic
- No dead code
- No hidden assumptions
- Performance unchanged or improved

---

# Definition of Done

A change is complete when:

- Specification implemented
- Tests pass
- Documentation matches implementation
- Acceptance criteria satisfied
- Review completed
- Ready for merge

Otherwise the change is incomplete.

---

# Final Principle

Protect the architecture.

Implementation exists to realize the specification, never to redefine it.