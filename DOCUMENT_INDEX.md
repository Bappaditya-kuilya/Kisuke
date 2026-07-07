# DOCUMENT INDEX

> Canonical navigation for the Kisuke repository.

---

# Reading Order

Always read documents in this order.

```
PROJECT_MANIFEST.md
        ↓
IMPLEMENTATION_CONTRACT.md
        ↓
CLAUDE.md
        ↓
MASTER_SPECIFICATION.md
        ↓
Supporting Documents
```

---

# Repository Documents

## Root

| Document | Purpose |
|----------|---------|
| PROJECT_MANIFEST.md | Project overview and architectural intent |
| IMPLEMENTATION_CONTRACT.md | Engineering rules |
| CLAUDE.md | Claude Code operating instructions |
| MASTER_SPECIFICATION.md | Navigation index into `docs/` (canonical specification) |
| README.md | Repository introduction |
| CHANGELOG.md | Version history |

---

# Documentation

## Foundation

```
docs/foundation/
```

| Document | Purpose |
|----------|---------|
| 00-vision.md | Product vision |
| 01-constitution.md | Immutable rules |
| 02-product-definition.md | Product scope |
| 03-product-rules.md | Product behavior |

---

## Architecture

```
docs/architecture/
```

| Document | Purpose |
|----------|---------|
| 04-domain-model.md | Canonical entities |
| 05-information-architecture.md | Information organization |
| 06-data-model.md | Metadata schema |
| 07-user-flows.md | User workflows |

---

## Engineering

```
docs/engineering/
```

| Document | Purpose |
|----------|---------|
| 08-cli-spec.md | CLI specification |
| 09-integrations.md | External integrations |
| 10-ai-abstraction.md | AI provider abstraction |
| 11-security.md | Security model |
| 12-engineering-architecture.md | Software architecture |

---

## Execution

```
docs/execution/
```

| Document | Purpose |
|----------|---------|
| 13-roadmap.md | Product roadmap |
| 14-implementation-plan.md | Milestones |
| 15-coding-guidelines.md | Coding standards |
| 16-testing-strategy.md | Testing strategy |
| 17-glossary.md | Terminology |
| 18-consistency-audit.md | Documentation consistency checklist |
| 19-repository-layout.md | Canonical on-disk structure |
| 99-architecture-audit.md | Final architecture validation |

---

# Supporting Directories

## ADRs

```
adrs/
```

Accepted architectural decisions.

---

## RFCs

```
rfcs/
```

Proposed architectural changes.

---

## Architecture

```
architecture/
```

Contains:

- Component diagrams
- Entity diagrams
- Sequence diagrams
- State machines

---

## Templates

```
templates/
```

Canonical Markdown templates.

---

## Source

```
src/
```

Application source code.

---

## Tests

```
tests/
```

Automated tests.

---

# Authority Order

The canonical authority order is defined once, in docs/foundation/01-constitution.md, § Authority. It is not restated here to avoid drift.

Implementation never overrides documentation.

---

# Implementation Order

There is exactly one implementation (build) order for Kisuke. It is defined once,
in docs/execution/13-roadmap.md, and restated here as the single canonical order:

```
Repository
        ↓
Domain
        ↓
Storage
        ↓
Parser & Validation
        ↓
Search
        ↓
Resume
        ↓
CLI
        ↓
Reviews
        ↓
Integrations
        ↓
AI
        ↓
Plugins
        ↓
Polish
```

No other document restates or redefines this order. The engineering *process*
(Idea → Specification → Implementation → Tests → Review → Merge) is a separate
concern and is defined once in IMPLEMENTATION_CONTRACT.md, not here.

---

# Rule

Every implementation task must be traceable to:

1. A section of the Master Specification.
2. A milestone.
3. A documented acceptance criterion.

If any of these are missing, implementation must stop.