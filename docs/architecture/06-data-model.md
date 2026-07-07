# Data Model

> Source: MASTER_SPECIFICATION.md §7

---

# Purpose

The Data Model defines the canonical structure of every entity stored by Kisuke.

It specifies logical data only.

It does not define implementation, databases, or serialization formats.

---

# Design Principles

The data model must be:

- Stable
- Explicit
- Immutable where possible
- Human-readable
- Provider-independent
- Markdown-first

---

# Universal Entity Schema

Every entity contains these fields. This schema applies to all eleven entities defined in the Domain Model, without exception.

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| id | UUID | ✓ | Globally unique identifier |
| type | Enum | ✓ | Entity type |
| title | String | ✓ | Human-readable title |
| owner | UUID or Reserved Owner Value | ✓ | Owning entity — see Owner Value Rules |
| status | Enum | ✓ | Current lifecycle state — see Entity Lifecycles |
| created_at | DateTime | ✓ | Creation timestamp |
| updated_at | DateTime | ✓ | Last modification |
| tags | List<String> | Optional | User tags |
| references | List<UUID> | Optional | Explicit relationships |
| attachments | List<UUID> | Optional | Attached binary assets |

There is no separate `archived` boolean. Archive state is one value of the `status` enum (`Archived`), not a second, independently-settable field. An entity is archived if, and only if, `status = Archived`. This applies uniformly, including to the four entities (Cookbook, Person, Resource, Attachment) that previously had no defined lifecycle — see Entity Lifecycles below, which now defines one for each.

---

# Owner Value Rules

Every entity's `owner` field must be a concrete value, even when the owner is not another domain entity instance.

| Owner Category | `owner` value |
|---|---|
| A specific domain entity instance (e.g. a Project owning a Task) | The UUID of that entity instance |
| Kisuke Core (Mission, Cookbook) | The reserved sentinel value `kisuke-core` |
| Independent (Meeting, Person, Resource) | The reserved sentinel value `independent` |
| Parent Entity (Attachment) | The UUID of the specific entity instance it is attached to (see Attachment Schema, field `owner`) |

Reserved sentinel values (`kisuke-core`, `independent`) are not UUIDs and never resolve to an entity record. Validation logic must treat them as valid, terminal owner values rather than as references to be dereferenced.

---

# Mission Schema

```yaml
id:
type: mission
title:
owner: kisuke-core
description:
status:
priority:
projects:
reviews:
created_at:
updated_at:
```

---

# Project Schema

```yaml
id:
type: project
title:
owner: mission-id
description:
status:
priority:
next_action:
tasks:
knowledge:
decisions:
meetings:
resources:
people:
created_at:
updated_at:
```

`owner` holds the ID of the owning Mission. The `mission` field used in earlier drafts is superseded by the Universal Entity Schema's `owner` field — there is one field for this relationship, not two.

---

# Task Schema

```yaml
id:
type: task
title:
owner: project-id
description:
status:
priority:
due_date:
estimated_time:
references:
created_at:
updated_at:
```

`owner` holds the ID of the owning Project.

---

# Knowledge Schema

```yaml
id:
type: knowledge
title:
owner: project-id
status:
summary:
content:
resources:
tags:
created_at:
updated_at:
```

`owner` holds the ID of the owning Project.

---

# Cookbook Schema

```yaml
id:
type: cookbook
title:
owner: kisuke-core
status:
content:
category:
tags:
references:
created_at:
updated_at:
```

---

# Decision Schema

```yaml
id:
type: decision
title:
owner: project-id
decision:
reason:
alternatives:
status:
created_at:
updated_at:
```

`owner` holds the ID of the owning Project.

---

# Meeting Schema

```yaml
id:
type: meeting
title:
owner: independent
status:
date:
people:
projects:
tasks:
decisions:
resources:
summary:
created_at:
updated_at:
```

`people` references the Person entities attending the meeting. This field was previously named `participants`; it is renamed here for consistency with the Domain Model's Meeting → Person relationship, which is the only relationship of its kind in this document. `people` contains references (IDs) only, per the Reference Rules.

---

# Person Schema

```yaml
id:
type: person
title:
owner: independent
status:
role:
organization:
email:
links:
notes:
created_at:
updated_at:
```

`title` holds the person's name (the Universal Entity Schema's human-readable title field; there is no separate `name` field).

---

# Resource Schema

```yaml
id:
type: resource
title:
owner: independent
status:
resource_type:
url:
description:
tags:
created_at:
updated_at:
```

`resource_type` holds the kind of source being referenced (Documentation, GitHub Repository, PDF, Website, Video, Dataset — see Domain Model, Resource entity). It is distinct from the Universal Entity Schema's `type` field, which always holds the entity type (`resource`) for every Resource instance. Earlier drafts used `type` for both purposes; this schema resolves that collision.

---

# Review Schema

```yaml
id:
type: review
title:
owner: mission-id
status:
review_type:
date:
summary:
completed_projects:
blocked_projects:
next_actions:
created_at:
updated_at:
```

`owner` holds the ID of the owning Mission. `review_type` holds the Review's kind (Morning, Weekly, Monthly, Quarterly), distinct from the Universal Entity Schema's `type` field (always `review`), for the same reason described under the Resource Schema.

---

# Attachment Schema

```yaml
id:
type: attachment
title:
owner:
status:
filename:
mime_type:
size:
checksum:
created_at:
updated_at:
```

`owner` holds the ID of the specific Parent Entity instance this Attachment is attached to (the field previously named `parent`; renamed for consistency with the Universal Entity Schema). `title` defaults to `filename` if not otherwise set.

---

# Metadata Rules

Every entity must include:

- Unique ID
- Type
- Owner
- Status
- Creation timestamp
- Last update timestamp

Optional metadata:

- Tags
- References
- Attachments

---

# Identifier Rules

IDs must:

- Be globally unique.
- Never change.
- Never be reused.
- Never encode business meaning.

UUIDv7 is recommended.

---

# Timestamp Rules

Store timestamps in UTC.

Fields:

- created_at
- updated_at

Optional:

- completed_at
- due_at

There is no `archived_at` field. The transition into the `Archived` status is recorded by `updated_at` like any other status transition; introducing a separate timestamp for one specific status value would duplicate what `status` + `updated_at` already record together.

---

# Status Values

## Mission

- Planning
- Active
- Completed
- Archived

---

## Project

- Planning
- Active
- Blocked
- Paused
- Completed
- Archived

---

## Task

- Todo
- In Progress
- Done
- Archived

---

## Knowledge

- Draft
- Active
- Deprecated
- Archived

---

## Decision

- Proposed
- Accepted
- Superseded
- Archived

---

## Meeting

- Scheduled
- Completed
- Archived

---

## Review

- Planned
- Completed
- Archived

---

## Cookbook

- Active
- Archived

---

## Person

- Active
- Archived

---

## Resource

- Active
- Unavailable
- Archived

`Unavailable` covers the case where the referenced external source can no longer be reached (see docs/architecture/07-user-flows.md, Failure Cases § Missing Resource: "Keep metadata. Mark resource unavailable."). This is a status transition, not a separate flag.

---

## Attachment

- Active
- Archived

---

# Reference Rules

References contain IDs only.

Never duplicate referenced content.

Allowed:

```yaml
references:
  - task-id
  - meeting-id
  - resource-id
```

Not allowed:

```yaml
references:
  - title: Git Docs
    url: ...
```

---

# Attachment Rules

Attachments:

- Always belong to one parent.
- Never exist independently.
- Never duplicate metadata stored elsewhere.

---

# Validation Rules

Every entity must satisfy:

- Valid UUID.
- Valid owner.
- Valid status.
- Existing references.
- No circular ownership.
- Immutable ID.

---

# Acceptance Criteria

The Data Model is complete when:

- Every entity has a schema.
- Required fields are defined.
- Metadata is standardized.
- Validation rules are documented.
- Relationships use IDs only.
- The model remains provider-independent.