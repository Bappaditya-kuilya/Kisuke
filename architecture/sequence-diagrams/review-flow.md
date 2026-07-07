# Review Flow

> Source: docs/architecture/07-user-flows.md (Flow 7 — Review), docs/execution/13-roadmap.md (M7 — Review System).

```mermaid
sequenceDiagram
    actor User
    participant CLI
    participant Review as Review Engine
    participant Domain
    participant Store as Markdown Storage

    User->>CLI: kisuke review weekly
    CLI->>Review: generate(type=Weekly)
    Review->>Store: load Mission + Projects
    Review->>Domain: inspect active / blocked projects
    Review->>Domain: compute Next Actions
    Domain-->>Review: review payload
    Review->>Store: write reviews/<id>.md (status: Completed)
    Review-->>CLI: review summary
    CLI-->>User: blockers + Next Actions
```

## Supported Reviews

- Morning
- Weekly
- Monthly
- Quarterly

A Review is owned by its Mission.
