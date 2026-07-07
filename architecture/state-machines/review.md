# Review State Machine

> Source: docs/architecture/04-domain-model.md (Entity Lifecycles), docs/architecture/06-data-model.md (Status Values).

## States

| State | Meaning |
|--------|---------|
| Planned | Scheduled |
| Completed | Evaluated |
| Archived | Historical |

## Transitions

```mermaid
stateDiagram-v2
    Planned --> Completed
    Completed --> Archived
```

Archiving is one-way through the `status` field; there is no separate `archived`
boolean.
