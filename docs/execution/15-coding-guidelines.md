# Coding Guidelines

> Source: MASTER_SPECIFICATION.md §16

---

# Purpose

This document defines the engineering standards for Kisuke.

Every contributor must follow these rules.

---

# General Principles

- Readability over cleverness.
- Simplicity over abstraction.
- Explicit over implicit.
- Composition over inheritance.
- Small functions.
- Small modules.

---

# Architecture Rules

Never violate:

- Clean Architecture
- Dependency Rule
- Single Ownership
- Reference over Duplication
- Markdown Canonical Storage

---

# Naming

Use meaningful names.

Good

```python
resume_project()
```

Bad

```python
rp()
```

Avoid abbreviations unless universally understood.

---

# File Size

Recommended

- <300 lines

Maximum

- 500 lines

Split when necessary.

---

# Function Size

Recommended

- <40 lines

Maximum

- 80 lines

Functions should do one thing.

---

# Classes

A class should have one responsibility.

Avoid God Objects.

---

# Comments

Comment **why**, not **what**.

Good

```python
# Prevent circular ownership.
```

Bad

```python
# Increment i.
i += 1
```

---

# Imports

- Standard Library
- Third-party
- Local

No wildcard imports.

---

# Errors

Return structured errors.

Never swallow exceptions.

Never fail silently.

---

# Logging

Log:

- Errors
- Warnings
- Important lifecycle events

Do not log:

- Secrets
- API Keys
- Tokens
- Personal data

---

# Testing

Every public function requires tests.

Bug fixes require regression tests.

---

# Dependencies

Before adding a dependency ask:

- Is it necessary?
- Can the standard library solve it?
- Is it maintained?
- Can it be replaced?

---

# Configuration

Never hardcode:

- Paths
- API Keys
- Secrets
- URLs

Use configuration.

---

# Markdown

Markdown is canonical.

Never edit generated artifacts directly.

---

# AI

Never call providers directly from business logic.

Always use the provider interface.

---

# Performance

Avoid premature optimization.

Optimize only after measurement.

---

# Code Review Checklist

- Correct
- Readable
- Tested
- Documented
- Simple
- No duplication
- No dead code

---

# Definition of Good Code

Good code is:

- Predictable
- Maintainable
- Testable
- Replaceable
- Easy to delete
- Easy to extend

---

# Final Rule

If a simpler solution exists that preserves the architecture, choose it.