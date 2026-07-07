# Kisuke Master Specification

> **Status:** Navigation Index (Frozen Architecture)
> **Role:** Routing index into `docs/`
> **Source of Truth:** `docs/` is the canonical specification.

---

# Purpose

This document is a **navigation index**. It does not restate specification content.

The canonical specification lives in `docs/`. Every section below routes to the
authoritative document there. This preserves a single source of truth and avoids
duplicated, drifting content.

Authority is defined once, in `docs/foundation/01-constitution.md`, § Authority.
That order is not restated here.

---

# Section Routing

| § | Topic | Canonical Document |
|---|-------|--------------------|
| §1 | Vision | `docs/foundation/00-vision.md` |
| §2 | Product Definition | `docs/foundation/02-product-definition.md` |
| §3 | Constitution | `docs/foundation/01-constitution.md` |
| §4 | Core Principles | `docs/foundation/00-vision.md`, `docs/foundation/02-product-definition.md` |
| §5 | Domain Model | `docs/architecture/04-domain-model.md` |
| §6 | Information Architecture | `docs/architecture/05-information-architecture.md` |
| §7 | Data Model | `docs/architecture/06-data-model.md` |
| §8 | User Flows | `docs/architecture/07-user-flows.md` |
| §9 | CLI Specification | `docs/engineering/08-cli-spec.md` |
| §10 | Integrations | `docs/engineering/09-integrations.md` |
| §11 | AI Abstraction | `docs/engineering/10-ai-abstraction.md` |
| §12 | Security | `docs/engineering/11-security.md` |
| §13 | Engineering Architecture | `docs/engineering/12-engineering-architecture.md` |
| §14 | Roadmap | `docs/execution/13-roadmap.md` |
| §15 | Implementation Plan | `docs/execution/14-implementation-plan.md` |
| §16 | Coding Guidelines | `docs/execution/15-coding-guidelines.md` |
| §17 | Testing Strategy | `docs/execution/16-testing-strategy.md` |
| §18 | ADR / RFC Index | `adrs/`, `rfcs/` |
| §19 | Architecture Audit | `docs/execution/99-architecture-audit.md` |

---

# Notes

- `MASTER_SPECIFICATION.md` is intentionally thin. It exists only to route.
- Implementation traces to `docs/`, not to this file.
- Any content copied here would drift; therefore no specification content is
  duplicated here.

---

# Final Principle

One specification, one authority, one source of truth: `docs/`.
