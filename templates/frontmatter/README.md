# Frontmatter Schemas

Canonical YAML frontmatter for every Kisuke entity, one file per entity.

Each schema matches `docs/architecture/06-data-model.md` and the Universal Entity
Schema defined there. The fields are:

- `id` — UUID (required)
- `type` — entity type Enum (required)
- `title` — human-readable title (required)
- `owner` — owning UUID or reserved sentinel (`kisuke-core`, `independent`) (required)
- `status` — lifecycle state Enum (required)
- `created_at` / `updated_at` — DateTime UTC (required)

Entity-specific fields are documented per file.

| File | Entity |
|------|--------|
| mission.yaml | Mission |
| project.yaml | Project |
| task.yaml | Task |
| knowledge.yaml | Knowledge |
| cookbook.yaml | Cookbook |
| decision.yaml | Decision |
| meeting.yaml | Meeting |
| person.yaml | Person |
| resource.yaml | Resource |
| review.yaml | Review |
| attachment.yaml | Attachment |

Reserved owner sentinels:

- `kisuke-core` — Mission, Cookbook
- `independent` — Meeting, Person, Resource

Archive state is one value of `status` (`Archived`). There is no separate
`archived` boolean and no `archived_at` timestamp.
