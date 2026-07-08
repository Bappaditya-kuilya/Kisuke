# Contributing to Kisuke

Thank you for your interest in contributing to Kisuke.

---

# Development Setup

1. Clone the repository
2. Install dependencies: `uv sync`
3. Run tests: `uv run pytest`

---

# Code Standards

- Follow the coding guidelines in `docs/execution/15-coding-guidelines.md`
- All code must pass Ruff linting
- All code must pass MyPy strict type checking
- All code must have tests

---

# Commit Messages

Use conventional commit format:

```
feat(module): description
fix(module): description
docs(section): description
refactor(module): description
test(module): description
```

One logical change per commit.

---

# Pull Requests

1. Create a feature branch
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request

Pull requests must:

- Preserve architecture
- Include tests
- Update documentation
- Pass all quality checks

---

# Architecture

Architecture changes require:

1. RFC
2. Review
3. ADR
4. Documentation update
5. Implementation

Never modify architecture through pull requests directly.

---

# Testing

Every feature requires:

- Unit tests
- Integration tests (when applicable)
- Acceptance verification

Bug fixes require regression tests.

---

# Documentation

All features must be documented.

Undocumented code is not accepted.

---

# Code Review

All pull requests require review before merge.

Review checklist:

- Architecture unchanged
- Documentation updated
- Tests passing
- No duplicated logic
- No dead code
- Performance unchanged or improved

---

# Questions?

Open a GitHub issue for questions about contributing.
