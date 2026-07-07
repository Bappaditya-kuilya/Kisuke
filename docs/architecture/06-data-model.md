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

Every entity contains these fields.

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| id | UUID | ✓ | Globally unique identifier |
| type | Enum | ✓ | Entity type |
| title | String | ✓ | Human-readable title |
| owner | UUID | ✓ | Owning entity |
| status | Enum | ✓ | Current lifecycle state |
| created_at | DateTime | ✓ | Creation timestamp |
| updated_at | DateTime | ✓ | Last modification |
| archived | Boolean | ✓ | Archive flag |
| tags | List<String> | Optional | User tags |
| references | List<UUID> | Optional | Explicit relationships |
| attachments | List<UUID> | Optional | Attached binary assets |

---

# Mission Schema

```yaml
id:
title:
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
mission:
title:
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

---

# Task Schema

```yaml
id:
project:
title:
description:
status:
priority:
due_date:
estimated_time:
references:
created_at:
updated_at:
```

---

# Knowledge Schema

```yaml
id:
project:
title:
summary:
content:
resources:
tags:
created_at:
updated_at:
```

---

# Cookbook Schema

```yaml
id:
title:
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
project:
title:
decision:
reason:
alternatives:
status:
created_at:
updated_at:
```

---

# Meeting Schema

```yaml
id:
title:
date:
participants:
projects:
tasks:
decisions:
resources:
summary:
created_at:
updated_at:
```

---

# Person Schema

```yaml
id:
name:
role:
organization:
email:
links:
notes:
created_at:
updated_at:
```

---

# Resource Schema

```yaml
id:
title:
type:
url:
description:
tags:
created_at:
updated_at:
```

---

# Review Schema

```yaml
id:
mission:
type:
date:
summary:
completed_projects:
blocked_projects:
next_actions:
created_at:
updated_at:
```

---

# Attachment Schema

```yaml
id:
parent:
filename:
mime_type:
size:
checksum:
created_at:
```

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
- archived_at
- due_at

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