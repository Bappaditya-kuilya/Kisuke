# Constitution

> Source: MASTER_SPECIFICATION.md §3

---

# Purpose

The Constitution defines the immutable architectural rules of Kisuke.

Every document, implementation, plugin, and integration must comply with these articles.

If any implementation conflicts with this Constitution, the Constitution prevails.

---

# Authority

This is the highest governing document of Kisuke.

Nothing may override it except an approved constitutional amendment.

Priority:

1. Constitution
2. PROJECT_MANIFEST.md
3. MASTER_SPECIFICATION.md
4. ADRs
5. Engineering Documents
6. Source Code

---

# Article I — Architecture is Frozen

The architecture of Kisuke is stable.

Implementation must realize the architecture, not redefine it.

---

# Article II — Documentation First

Documentation precedes implementation.

Code follows documentation.

Documentation never follows code.

---

# Article III — Markdown is the Source of Truth

Markdown files are the authoritative representation of Kisuke's knowledge.

Indexes, caches, databases, and AI outputs are derived artifacts.

---

# Article IV — Git Owns History

Git is the only historical record.

Kisuke must never implement a competing history system.

---

# Article V — Single Ownership

Every entity has exactly one owner.

Ownership is explicit.

Ownership never changes implicitly.

---

# Article VI — References over Duplication

Relationships are represented using references.

Duplicating information to express relationships is forbidden.

---

# Article VII — Local First

Core functionality operates without network connectivity.

Cloud capabilities are optional enhancements.

---

# Article VIII — Resume Before Search

The primary goal is context reconstruction.

Search exists only to support resumption.

---

# Article IX — Integration Before Rebuilding

If an existing tool already performs a capability well, Kisuke integrates with it instead of replacing it.

---

# Article X — AI Owns Nothing

AI processes information.

AI never becomes the owner or source of truth for any data.

---

# Article XI — Core Simplicity

The core remains small, opinionated, and stable.

New capabilities belong in adapters or plugins whenever possible.

---

# Amendment Process

The Constitution may only change through:

```
RFC

↓

Review

↓

ADR

↓

MASTER_SPECIFICATION Update

↓

Implementation
```

Implementation may never change the Constitution directly.

---

# Compliance Checklist

Every architectural decision must satisfy:

- Architecture preserved
- Single ownership maintained
- No duplicated data
- Markdown remains authoritative
- Git remains historical source
- AI remains optional
- Core remains provider-independent

If any answer is **No**, the change is rejected.

---

# Final Principle

Protect the architecture.

Everything else is negotiable.