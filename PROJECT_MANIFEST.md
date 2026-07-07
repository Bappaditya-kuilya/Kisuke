# PROJECT MANIFEST

## Project

**Name:** Kisuke

**Status:** Architecture Frozen (v1)

---

# Purpose

Kisuke is a local-first context reconstruction system.

Its purpose is to reduce the time and mental effort required to resume meaningful work.

---

# Core Promise

> Kisuke does not return notes.

> Kisuke returns working context.

---

# Source of Truth

Priority order:

1. Constitution
2. ADRs
3. Architecture documents
4. Engineering documents
5. Implementation

If code conflicts with documentation, the documentation wins.

---

# Repository Structure

* `docs/` — Product and engineering specifications.
* `adrs/` — Accepted architecture decisions.
* `rfcs/` — Proposed future changes.
* `architecture/` — Diagrams and models.
* `templates/` — Markdown and frontmatter templates.
* `src/` — Implementation.
* `tests/` — Test suite.

---

# Non-Negotiable Rules

* Architecture is frozen.
* Markdown is the source of truth.
* Git owns history.
* AI owns no data.
* Every entity has one owner.
* Relationships use references.
* Offline-first.
* Resume before search.
* Integrate before rebuilding.

---

# Current Phase

Documentation Expansion

No implementation changes are allowed until documentation passes architecture review.

---

# Definition of Success

A new engineer can implement Kisuke correctly using only this repository.
