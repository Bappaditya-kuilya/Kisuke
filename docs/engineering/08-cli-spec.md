# CLI Specification

> Source: MASTER_SPECIFICATION.md §9

---

# Purpose

The Kisuke CLI provides a fast, keyboard-first interface for interacting with the system.

The CLI is the primary interface.

GUI support is secondary.

---

# Design Principles

The CLI must be:

- Fast
- Predictable
- Scriptable
- Human-readable
- Composable
- Offline-first

---

# Command Structure

```
kisuke <command> <subcommand> [options]
```

Examples

```
kisuke resume
kisuke project list
kisuke task next
kisuke review weekly
kisuke search docker
```

---

# Global Options

```
--help
--version
--verbose
--json
--quiet
```

---

# Top-Level Commands

```
kisuke init
kisuke doctor
kisuke status
kisuke config
kisuke resume
kisuke mission
kisuke project
kisuke task
kisuke knowledge
kisuke cookbook
kisuke decision
kisuke meeting
kisuke resource
kisuke review
kisuke search
kisuke sync
kisuke plugin
kisuke index
```

---

# Resume

```
kisuke resume
```

Opens the current working context.

Options

```
--mission
--project
--last
```

---

# Mission

```
kisuke mission create
kisuke mission list
kisuke mission show
kisuke mission archive
```

---

# Project

```
kisuke project create
kisuke project list
kisuke project show
kisuke project open
kisuke project archive
```

---

# Task

```
kisuke task add
kisuke task list
kisuke task next
kisuke task done
kisuke task move
```

---

# Knowledge

```
kisuke knowledge add
kisuke knowledge list
kisuke knowledge open
```

---

# Cookbook

```
kisuke cookbook add
kisuke cookbook search
kisuke cookbook open
```

---

# Decision

```
kisuke decision add
kisuke decision list
kisuke decision show
```

---

# Meeting

```
kisuke meeting add
kisuke meeting today
kisuke meeting list
```

---

# Review

```
kisuke review morning
kisuke review weekly
kisuke review monthly
kisuke review quarterly
```

---

# Search

```
kisuke search <query>
```

Options

```
--project
--cookbook
--knowledge
--decision
--resource
```

---

# Resource

```
kisuke resource add
kisuke resource list
kisuke resource open
```

---

# Index

```
kisuke index build
kisuke index update
kisuke index clean
```

---

# Plugin

```
kisuke plugin list
kisuke plugin install
kisuke plugin remove
kisuke plugin update
```

---

# Config

```
kisuke config get
kisuke config set
kisuke config edit
```

---

# Doctor

```
kisuke doctor
```

Checks:

- Repository
- Markdown
- Index
- Configuration
- Plugins

---

# Output Rules

Default:

Human-readable.

Optional:

```
--json
```

returns machine-readable output.

---

# Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General Error |
| 2 | Invalid Arguments |
| 3 | Not Found |
| 4 | Validation Error |
| 5 | Permission Error |

---

# Performance Targets

CLI startup:

<200 ms

Command execution:

<500 ms

Search:

<500 ms (warm index)

---

# Acceptance Criteria

- Every command is deterministic.
- Commands are composable.
- Output is script-friendly.
- All core workflows are accessible from the CLI.
- Core functionality works offline.