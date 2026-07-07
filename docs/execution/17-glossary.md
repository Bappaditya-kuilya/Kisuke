# Glossary

> Source: MASTER_SPECIFICATION.md §18

---

# Purpose

This glossary defines the canonical meaning of terms used throughout Kisuke.

These definitions are authoritative.

---

# Mission

A long-term objective that provides strategic direction.

Owns:

- Projects
- Reviews

Example

```
Become an AI Engineer
```

---

# Project

A temporary endeavor with a defined beginning and end undertaken to create a unique outcome.

Owns:

- Tasks
- Knowledge
- Decisions

Example

```
Build Kisuke
```

---

# Task

The smallest executable unit of work.

Belongs to exactly one Project.

Example

```
Implement Resume Engine
```

---

# Next Action

The single highest-priority executable Task for an active Project.

Each active Project may have only one Next Action.

---

# Knowledge

Project-specific information created or collected during execution.

Example

- Research
- Notes
- Findings
- Explanations

---

# Cookbook

Evergreen reusable knowledge.

Independent of any Project.

Example

- Git commands
- Linux commands
- Docker snippets

---

# Decision

A recorded explanation of why a particular choice was made.

Includes:

- Decision
- Reason
- Alternatives

---

# Meeting

A time-bounded discussion.

Meetings reference entities.

They own none.

---

# Person

An individual associated with work.

Examples

- Mentor
- Recruiter
- Client
- Team Member

---

# Resource

An external source of information.

Examples

- Website
- PDF
- GitHub Repository
- Video
- Documentation

---

# Review

A structured evaluation of current work.

Types

- Morning
- Weekly
- Monthly
- Quarterly

---

# Attachment

A binary asset belonging to another entity.

Examples

- Image
- PDF
- ZIP
- Screenshot

---

# Context

The minimum information required to continue meaningful work.

Includes:

- Current state
- Next Action
- Decisions
- Knowledge
- Resources

---

# Context Reconstruction

The deterministic process of rebuilding working context from stored entities and relationships.

This is Kisuke's primary capability.

---

# Resume

The act of restoring working context so work can continue immediately.

---

# Ownership

The explicit responsibility assigned to an entity.

Every entity has exactly one owner.

---

# Relationship

An explicit reference between two entities.

Relationships never imply ownership.

---

# Markdown

The canonical storage format.

All derived artifacts originate from Markdown.

---

# Derived Artifact

Data generated from canonical Markdown.

Examples

- SQLite index
- Cache
- Embeddings
- Search index

Derived artifacts may be rebuilt at any time.

---

# Provider

An external implementation of a service.

Examples

- OpenAI
- Anthropic
- Gemini
- Ollama

Providers are replaceable.

---

# Adapter

A software component that connects Kisuke to an external system while preserving the architecture.

---

# Plugin

An optional extension that adds capabilities without modifying the Core.

Plugins may extend behavior.

They may not redefine architecture.

---

# Core

The domain and application logic of Kisuke.

Core has no dependency on:

- AI providers
- Databases
- Editors
- External services

---

# Architecture Drift

Any implementation that changes the documented architecture without following the RFC and ADR process.

Architecture drift is prohibited.

---

# Source of Truth

The authoritative representation of information.

Within Kisuke:

- Markdown is the source of truth.
- Git is the source of history.
- AI is never a source of truth.

---

# Final Principle

Every term in Kisuke has one canonical meaning.

Terminology must remain consistent across documentation, implementation, tests, and user interfaces.