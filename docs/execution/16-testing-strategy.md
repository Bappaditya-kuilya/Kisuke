# Testing Strategy

> Source: MASTER_SPECIFICATION.md §17

---

# Purpose

This document defines the testing strategy for Kisuke.

Testing ensures architectural correctness, functional correctness, and long-term maintainability.

---

# Principles

- Test behavior, not implementation.
- Automate everything possible.
- Small tests first.
- Deterministic tests.
- Fast feedback.
- Every bug gets a regression test.

---

# Testing Pyramid

```text
           E2E
      Integration
         Unit
```

Target distribution

| Type | Target |
|-------|--------|
| Unit | 70% |
| Integration | 20% |
| End-to-End | 10% |

---

# Unit Testing

Tests:

- Domain Entities
- Value Objects
- Validation
- Parsers
- Utilities

Requirements

- No filesystem
- No network
- No AI
- No database

Execution time:

<1 second

---

# Integration Testing

Tests interaction between components.

Examples

- Markdown ↔ Parser
- Parser ↔ Domain
- Search ↔ Index
- CLI ↔ Application
- Integrations ↔ Adapters

Use temporary files.

Never modify user data.

---

# End-to-End Testing

Validate complete workflows.

Required flows

- Resume Project
- Create Project
- Add Task
- Record Decision
- Perform Review
- Search
- Archive

---

# AI Testing

Use mocks.

Never depend on:

- Internet
- Provider availability
- API Keys

Test:

- Prompt generation
- Context preparation
- Provider interface
- Error handling

---

# CLI Testing

Verify

- Commands
- Exit codes
- JSON output
- Help output
- Invalid arguments

---

# Performance Testing

Measure

- CLI startup
- Search
- Resume
- Parsing
- Indexing

Targets

| Operation | Target |
|-----------|---------|
| CLI Startup | <200 ms |
| Search | <500 ms |
| Resume | <2 s |
| Parse | Incremental |

---

# Validation Testing

Verify

- Ownership
- References
- Lifecycles
- Required metadata
- UUID uniqueness

Reject invalid repositories.

---

# Regression Testing

Every bug fix must include:

1. Failing test.
2. Fix.
3. Passing test.

Never fix without a test.

---

# Test Data

Test repositories must be:

- Small
- Predictable
- Version controlled
- Disposable

Never use personal data.

---

# Continuous Integration

Every pull request runs:

- Formatting
- Linting
- Type checking
- Unit tests
- Integration tests

Merge blocked on failure.

---

# Coverage

Minimum goals

| Layer | Coverage |
|--------|----------|
| Domain | 95% |
| Application | 90% |
| Infrastructure | 85% |
| Integrations | 80% |

Coverage is a signal, not the goal.

---

# Acceptance Criteria

Testing is complete when:

- All tests pass.
- Critical paths are covered.
- Performance targets are met.
- No flaky tests exist.
- CI passes consistently.

---

# Final Principle

If it cannot be tested reliably, it should not be implemented.