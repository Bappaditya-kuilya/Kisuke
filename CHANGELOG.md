# Changelog

All notable changes to Kisuke will be documented here.

The format follows Keep a Changelog.

---

## [Unreleased]

### Added

- Initial repository
- Master Specification
- ADR system
- RFC system
- Documentation structure

---

## [0.1.0] - 2026-07-08

### Added

- Domain model (Mission, Project, Task, Knowledge, Cookbook, Decision, Meeting, Person, Resource, Review, Attachment)
- Markdown storage with lossless round-trip
- Parser and validation (schema, reference, ownership, lifecycle)
- Search engine with incremental indexing
- Resume engine for context reconstruction
- CLI with all core workflows
- Review system (morning, weekly, monthly, quarterly)
- Integrations (Git, filesystem watcher, markdown import/export, sync)
- AI abstraction layer (provider interface, registry, local provider, OpenAI-compatible adapter)
- Plugin system for safe extensibility
- Comprehensive test suite
- Documentation coverage

### Changed

- None

### Deprecated

- None

### Removed

- None

### Fixed

- None

### Security

- Secrets never committed to version control
- Environment variables only for configuration
- No hidden telemetry
- Local-first operation by default

---

## [0.0.1] - 2026-07-01

### Added

- Repository bootstrap
- Build system
- Test framework
- Documentation structure
