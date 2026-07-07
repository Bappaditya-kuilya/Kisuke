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
| MASTER_SPECIFICATION.md | Complete architecture and product specification |
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

When two documents disagree:

```
Constitution
        ↓
PROJECT_MANIFEST.md
        ↓
MASTER_SPECIFICATION.md
        ↓
ADRs
        ↓
Engineering Docs
        ↓
Implementation
```

Implementation never overrides documentation.

---

# Development Order

```
Repository
        ↓
Master Specification
        ↓
Architecture Review
        ↓
Documentation
        ↓
Implementation
        ↓
Testing
        ↓
Release
```

---

# Milestone Order

```
M0 Repository
        ↓
M1 Domain
        ↓
M2 Storage
        ↓
M3 CLI
        ↓
M4 Resume
        ↓
M5 Search
        ↓
M6 Review
        ↓
M7 Integrations
        ↓
M8 AI
        ↓
M9 Plugins
```

---

# Rule

Every implementation task must be traceable to:

1. A section of the Master Specification.
2. A milestone.
3. A documented acceptance criterion.

If any of these are missing, implementation must stop.