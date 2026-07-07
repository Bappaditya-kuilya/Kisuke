# DOCUMENT INDEX

## Purpose

This document is the navigation entry point for the Kisuke documentation.

It defines the reading order, document authority, and dependency graph. Every contributor and AI assistant should use this file to understand where to start and how the documentation is organized.

---

# Reading Order

Read the documentation in this exact order.

## Level 0 — Repository

1. PROJECT_MANIFEST.md
2. IMPLEMENTATION_CONTRACT.md
3. CLAUDE.md

---

## Level 1 — Foundation

1. docs/foundation/00-vision.md
2. docs/foundation/01-constitution.md
3. docs/foundation/02-product-definition.md
4. docs/foundation/03-product-rules.md

Purpose:

Defines why Kisuke exists and the immutable rules of the system.

---

## Level 2 — Architecture

1. docs/architecture/04-domain-model.md
2. docs/architecture/05-information-architecture.md
3. docs/architecture/06-data-model.md
4. docs/architecture/07-user-flows.md

Purpose:

Defines the business model, ownership, relationships, metadata, and behavior.

---

## Level 3 — Engineering

1. docs/engineering/08-cli-spec.md
2. docs/engineering/09-integrations.md
3. docs/engineering/10-ai-abstraction.md
4. docs/engineering/11-security.md
5. docs/engineering/12-engineering-architecture.md

Purpose:

Defines how the system is implemented while preserving the architecture.

---

## Level 4 — Execution

1. docs/execution/13-roadmap.md
2. docs/execution/14-implementation-plan.md
3. docs/execution/15-coding-guidelines.md
4. docs/execution/16-testing-strategy.md
5. docs/execution/17-glossary.md
6. docs/execution/99-architecture-audit.md

Purpose:

Defines the implementation process, engineering standards, and long-term maintenance.

---

## Supporting Documents

### Architecture Decisions

Directory:

```text
adrs/
```

Purpose:

Permanent record of accepted architectural decisions.

---

### RFCs

Directory:

```text
rfcs/
```

Purpose:

Proposals for future architectural or product changes before implementation.

---

### Architecture Diagrams

Directory:

```text
architecture/
```

Purpose:

System diagrams, entity relationships, state machines, sequence diagrams, and component views.

---

### Templates

Directory:

```text
templates/
```

Purpose:

Canonical Markdown and frontmatter templates for every entity.

---

# Document Authority

If documents disagree, resolve conflicts using this order:

1. Constitution
2. ADRs
3. Domain Model
4. Engineering Architecture
5. Other documentation
6. Source Code

Source code never overrides the Constitution.

---

# Dependency Graph

```text
Vision
    ↓
Constitution
    ↓
Product Definition
    ↓
Domain Model
    ↓
Information Architecture
    ↓
Data Model
    ↓
User Flows
    ↓
Engineering Architecture
    ↓
Implementation Plan
    ↓
Source Code
```

---

# Contributor Rules

Before implementing any feature:

1. Read the relevant documentation.
2. Verify the architecture is not being changed.
3. Confirm the feature belongs to the current milestone.
4. Update documentation if behavior changes.
5. Add or update tests before merging.

---

# Completion Criteria

The documentation repository is considered complete when:

* Every document is internally consistent.
* No architectural contradictions exist.
* Every implementation task can be traced back to a document.
* A new engineer can implement Kisuke without additional product clarification.
