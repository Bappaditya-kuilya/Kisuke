# Repository Layout

> Canonical on-disk structure for Kisuke.

## Principles

- Markdown is canonical.
- One entity = one file.
- IDs are immutable.
- References use IDs.
- No duplicated data.

---

# Repository

```
kisuke-data/
│
├── missions/
│   ├── <mission-id>.md
│   └── ...
│
├── projects/
│   ├── <project-id>.md
│   └── ...
│
├── tasks/
│   ├── <task-id>.md
│   └── ...
│
├── knowledge/
│   ├── <knowledge-id>.md
│   └── ...
│
├── cookbook/
│   ├── <entry-id>.md
│   └── ...
│
├── decisions/
│   ├── <decision-id>.md
│   └── ...
│
├── meetings/
│   ├── <meeting-id>.md
│   └── ...
│
├── people/
│   ├── <person-id>.md
│   └── ...
│
├── reviews/
│   ├── <review-id>.md
│   └── ...
│
├── resources/
│   ├── <resource-id>.md
│   └── ...
│
├── attachments/
│
├── index/
│
├── cache/
│
└── config/
```

---

# Rules

- Every Markdown file represents one entity.
- Folder names never change.
- Entity IDs never change.
- Relationships are stored by ID only.
- Attachments never contain metadata duplicated elsewhere.
- `index/` and `cache/` are rebuildable.
- `config/` is local configuration only.