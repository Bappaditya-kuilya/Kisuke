# Capture Flow

> Source: docs/architecture/07-user-flows.md (Flow 2 — Capture Information), docs/engineering/12-engineering-architecture.md (Storage Architecture).

Capture must be frictionless. Classification never blocks capture.

```mermaid
sequenceDiagram
    actor User
    participant CLI
    participant App as Application Service
    participant Domain
    participant Store as Markdown Storage

    User->>CLI: kisuke <entity> add
    CLI->>App: create entity (frontmatter + body)
    App->>Domain: validate (owner, status, references)
    Domain-->>App: valid
    App->>Store: write <type>/<id>.md
    Store-->>App: saved
    App-->>CLI: success (id)
    CLI-->>User: entity created
```

## Rules

- One entity = one Markdown file.
- Relationships stored by ID only.
- Derived index/cache are rebuilt, never authored by capture.
