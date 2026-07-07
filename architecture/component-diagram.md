# Component Diagram

> Source: docs/engineering/12-engineering-architecture.md (High-Level Architecture, Layers, Core/Infrastructure/Integration Modules).

## Layered View

Dependencies always point inward. The Domain depends on nothing.

```text
                User
                  │
                  ▼
         CLI / Future UI  (Presentation)
                  │
                  ▼
        Application Services
                  │
                  ▼
          Domain (Core)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Infrastructure      Integrations
        │                   │
        ▼                   ▼
 Storage / Index      Git, AI, Calendar,
                       Obsidian, VS Code
```

## Module Map

```text
core/
├── domain/
├── application/
├── storage/
├── search/
├── resume/
├── review/
├── parser/
└── validation/

infrastructure/
├── markdown/
├── sqlite/
├── filesystem/
├── cache/
└── indexing/

integrations/
├── git/
├── github/
├── obsidian/
├── vscode/
├── calendar/
└── ai/

plugins/
├── interfaces/
├── registry/
└── loader/
```

## Dependencies

- Presentation depends on Application.
- Application depends on Domain.
- Infrastructure implements interfaces defined by Domain.
- Integrations are never accessed directly by the Domain.
- Plugins are isolated and never modify the Core directly.

## Storage / Search / Resume Paths

```text
Markdown ─▶ Parser ─▶ Domain Objects ─▶ Search Index
Project ─▶ Relationships ─▶ Current State ─▶ Next Action ─▶ Context Bundle
```
