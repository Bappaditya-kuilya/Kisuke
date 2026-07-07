# Entity Relationship

> Source: docs/architecture/04-domain-model.md (Ownership Model, Relationship Model, Cardinality).

## Ownership Hierarchy

Every entity has exactly one owner. Ownership categories `Kisuke Core`,
`Independent`, and `Parent Entity` are not entity instances and have no UUID.

```text
Kisuke Core
├── Mission
│   ├── Project
│   │   ├── Task
│   │   ├── Knowledge
│   │   └── Decision
│   └── Review
│
└── Cookbook

Independent
├── Meeting
├── Person
└── Resource

Parent Entity
└── Attachment
```

## Owner Values

| Entity | Owner |
|--------|-------|
| Mission | Kisuke Core (`kisuke-core`) |
| Project | Mission |
| Task | Project |
| Knowledge | Project |
| Cookbook | Kisuke Core (`kisuke-core`) |
| Decision | Project |
| Meeting | Independent (`independent`) |
| Person | Independent (`independent`) |
| Resource | Independent (`independent`) |
| Review | Mission |
| Attachment | Parent Entity (specific UUID) |

## Relationship Cardinality

Relationships are references (IDs), never duplicates.

| Relationship | Cardinality |
|-------------|------------|
| Mission → Project | 1:N |
| Mission → Review | 1:N |
| Project → Task | 1:N |
| Project → Knowledge | 1:N |
| Project → Decision | 1:N |
| Project → Meeting | N:N |
| Project → Resource | N:N |
| Project → Person | N:N |
| Cookbook → Knowledge | 1:N |
| Cookbook → Resource | N:N |
| Knowledge → Resource | N:N |
| Decision → Project | N:N |
| Decision → Resource | N:N |
| Decision → Meeting | N:N |
| Meeting → Project | N:N |
| Meeting → Task | N:N |
| Meeting → Decision | N:N |
| Meeting → Person | N:N |
| Meeting → Resource | N:N |
| Review → Mission | N:N |
| Review → Project | N:N |
| Review → Task | N:N |

## Invariants

- References never imply ownership.
- References are directional.
- Every reference points to an existing entity.
- Circular ownership is forbidden; circular *relationships* are allowed only
  when they do not create circular ownership.
- Deleted entities must remove or update dangling references.
