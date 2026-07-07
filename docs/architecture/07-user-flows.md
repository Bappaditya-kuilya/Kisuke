# User Flows

> Source: MASTER_SPECIFICATION.md §8

---

# Purpose

This document defines the primary user workflows of Kisuke.

Every workflow must reduce context reconstruction effort.

---

# Design Principles

Every workflow should:

- Minimize clicks.
- Minimize searching.
- Preserve context.
- Never duplicate information.
- End with a clear Next Action.

---

# Primary Workflows

1. Resume Work
2. Capture Information
3. Create Project
4. Complete Task
5. Record Decision
6. Conduct Meeting
7. Perform Review
8. Search
9. Archive

---

# Flow 1 — Resume Work

```
Open Kisuke
      ↓
Resume Dashboard
      ↓
Select Project
      ↓
Context Reconstruction
      ↓
Understand Current State
      ↓
Next Action
      ↓
Continue Working
```

Context includes:

- Mission
- Project
- Current Status
- Next Action
- Active Tasks
- Recent Decisions
- Relevant Knowledge
- Recent Meetings
- Resources

---

# Flow 2 — Capture Information

```
Capture
    ↓
Select Entity Type
    ↓
Link References
    ↓
Save
```

Capture must be frictionless.

Classification never blocks capture.

---

# Flow 3 — Create Project

```
Choose Mission
      ↓
Create Project
      ↓
Set Status
      ↓
Add First Task
      ↓
Set Next Action
```

---

# Flow 4 — Complete Task

```
Open Task
     ↓
Mark Done
     ↓
Update Project State
     ↓
Recommend Next Action
```

Only one Next Action may exist.

---

# Flow 5 — Record Decision

```
Create Decision
      ↓
Record Reason
      ↓
Record Alternatives
      ↓
Link Resources
      ↓
Save
```

Every important decision should be documented.

---

# Flow 6 — Meeting

```
Create Meeting
      ↓
Link Project
      ↓
Record Discussion
      ↓
Create Decisions
      ↓
Create Tasks
      ↓
Complete
```

Meetings never own Tasks or Decisions.

They reference them.

---

# Flow 7 — Review

```
Start Review
      ↓
Inspect Mission
      ↓
Inspect Projects
      ↓
Inspect Blockers
      ↓
Update Next Actions
      ↓
Complete Review
```

Supported Reviews:

- Morning
- Weekly
- Monthly
- Quarterly

---

# Flow 8 — Search

```
Query
   ↓
Current Project
   ↓
Mission
   ↓
Cookbook
   ↓
Global Search
```

Search supports resume.

Search does not replace resume.

---

# Flow 9 — Archive

```
Select Entity
      ↓
Validate References
      ↓
Archive
```

Archiving preserves history.

Deletion is exceptional.

---

# Failure Cases

## Missing Project

Return:

Project not found.

---

## Broken Reference

Display warning.

Never silently remove references.

---

## Missing Resource

Keep metadata.

Mark resource unavailable.

---

## AI Unavailable

Continue normally.

AI is optional.

---

# Acceptance Criteria

Every workflow must:

- Preserve ownership.
- Preserve references.
- Preserve history.
- Maintain a single Next Action.
- Complete without AI.
- Minimize cognitive load.

---

# Final Principle

A user should always know:

- Where they are.
- Why they are there.
- What to do next.
- What information matters now.