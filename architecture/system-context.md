# System Context

> Scope: how Kisuke sits in its operating environment.
> Source: docs/engineering/12-engineering-architecture.md.

## Actors

- **User** — a developer, builder, or researcher who switches between projects
  and needs to resume work with minimal cognitive overhead.

## Kisuke (the system)

Kisuke is a local-first context reconstruction system. Its core promise:

> Kisuke does not return notes. Kisuke returns working context.

Core capabilities:

- Context reconstruction (Resume)
- Capture
- Search (supports resume)
- Reviews
- Optional AI summarization / classification

## External Systems (integrations, all optional)

Kisuke integrates rather than rebuilds. The Domain never depends on any of these.

- Git / GitHub — history and remote sync
- Obsidian — note access
- VS Code — editor integration
- Google Calendar — scheduling
- AI Providers (OpenAI, Anthropic, Gemini, Ollama) — optional enhancement only

## Boundaries

```text
        +-------------------+
        |       User        |
        +-------------------+
                 │
                 ▼
        +-------------------+
        |      Kisuke       |   Local-first, offline-capable
        |  (Core + CLI)     |
        +-------------------+
           │     │     │
   ┌───────┘     │     └────────┐
   ▼             ▼              ▼
 Git/GitHub   Obsidian/VS Code   AI Providers
                          (Google Calendar)
```

## Key Properties

- Markdown is the source of truth.
- Git owns history.
- AI owns nothing; it is optional.
- Core functions without any integration.
- Architecture is frozen (Non-Negotiable Rule 1).
