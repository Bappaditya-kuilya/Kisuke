# Architecture Audit

> Purpose: Verify that the implemented system conforms to the documented architecture before every release.

---

# Scope

This audit validates:

- Architecture
- Domain Model
- Information Architecture
- Data Model
- Engineering Architecture
- Security
- Testing
- Implementation

It does **not** review feature quality.

---

# Audit Principles

- Architecture is authoritative.
- Documentation precedes implementation.
- Every violation must be traceable.
- Every finding must have evidence.

---

# Audit Levels

## Critical

Violates the Constitution.

Examples

- Multiple ownership
- Markdown no longer canonical
- Core depends on AI provider
- Hidden architecture change

Release is blocked.

---

## Major

Architecture preserved but implementation quality is compromised.

Examples

- Missing validation
- Circular dependency
- Untested critical path
- Performance regression

Must be fixed before release.

---

## Minor

Non-blocking improvements.

Examples

- Naming inconsistencies
- Missing documentation
- Small refactoring opportunities

Can be scheduled.

---

# Audit Checklist

## Repository

- Repository structure matches specification.
- Required documents exist.
- Documentation is synchronized.

---

## Domain

- All entities implemented.
- Ownership preserved.
- Relationships preserved.
- Lifecycles implemented.
- Invariants enforced.

---

## Storage

- Markdown remains canonical.
- Derived artifacts rebuild correctly.
- No duplicated data.

---

## Resume Engine

- Context reconstruction deterministic.
- Next Action computed correctly.
- Context ordering preserved.

---

## Search

- Search returns expected entities.
- Ranking deterministic.
- Index rebuild successful.

---

## CLI

- Every documented command implemented.
- Exit codes correct.
- Help output complete.
- JSON output valid.

---

## Integrations

- All integrations optional.
- Core functions without integrations.
- Integration failures isolated.

---

## AI

- Provider abstraction preserved.
- AI optional.
- No provider-specific logic in Core.
- No automatic data ownership.

---

## Plugins

- Plugins isolated.
- Public interfaces respected.
- Core remains unchanged.

---

## Security

- Secrets protected.
- No hidden telemetry.
- Least privilege maintained.
- Markdown integrity preserved.

---

## Testing

- Unit tests passing.
- Integration tests passing.
- End-to-end tests passing.
- Regression tests present.

---

## Performance

Verify targets.

| Operation | Target |
|-----------|---------|
| CLI Startup | <200 ms |
| Search | <500 ms |
| Resume | <2 s |
| Incremental Index | Working |

---

# Compliance Matrix

| Area | Pass | Fail | Notes |
|------|------|------|-------|
| Constitution | ☐ | ☐ | |
| Domain | ☐ | ☐ | |
| Storage | ☐ | ☐ | |
| Resume | ☐ | ☐ | |
| Search | ☐ | ☐ | |
| CLI | ☐ | ☐ | |
| Integrations | ☐ | ☐ | |
| AI | ☐ | ☐ | |
| Plugins | ☐ | ☐ | |
| Security | ☐ | ☐ | |
| Testing | ☐ | ☐ | |
| Documentation | ☐ | ☐ | |

---

# Release Gate

A release is approved only if:

- No Critical findings.
- No unresolved Major findings.
- Documentation synchronized.
- All tests passing.
- Performance targets met.
- Architecture unchanged.

Otherwise:

Release is rejected.

---

# Audit Report Template

```text
Architecture Audit Report

Date:
Version:
Auditor:

Critical:
- None

Major:
- None

Minor:
- None

Recommendations:

Result:
PASS / FAIL
```

---

# Final Principle

Architecture is a contract.

Every release must prove compliance with that contract before it is considered complete.