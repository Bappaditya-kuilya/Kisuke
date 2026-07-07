# Resume Flow

> Source: docs/architecture/07-user-flows.md (Flow 1 — Resume Work), docs/architecture/05-information-architecture.md (Resume Order, Context Stack), docs/engineering/12-engineering-architecture.md (Resume Architecture).

The primary capability of Kisuke. Deterministic context reconstruction.

```mermaid
sequenceDiagram
    actor User
    participant CLI
    participant Resume as Resume Engine
    participant Domain
    participant Store as Markdown Storage
    participant Index as Search Index

    User->>CLI: kisuke resume [--project]
    CLI->>Resume: reconstruct(context)
    Resume->>Store: load Project + Mission
    Resume->>Domain: traverse relationships
    Domain->>Store: fetch Tasks, Decisions, Knowledge, Meetings, Resources
    Resume->>Domain: compute Next Action
    Domain-->>Resume: ordered Context Stack
    Resume-->>CLI: Context Bundle
    CLI-->>User: current state + Next Action
```

## Resume Order (fixed)

1. Mission
2. Project
3. Project Status
4. Current State
5. Next Action
6. Active Tasks
7. Recent Decisions
8. Relevant Knowledge
9. Related Meetings
10. Related Resources
11. Attachments

## Performance Target

Resume < 2 seconds (warm cache).
