# Task State Machine

> Source: docs/architecture/04-domain-model.md (Entity Lifecycles), docs/architecture/06-data-model.md (Status Values).

## States

| State | Meaning |
|--------|---------|
| Todo | Not started |
| In Progress | Being worked |
| Done | Completed |
| Archived | Historical |

## Transitions

```mermaid
stateDiagram-v2
    Todo --> InProgress
    InProgress --> Done
    Done --> Archived
```

Archiving is one-way through the `status` field; there is no separate `archived`
boolean.
