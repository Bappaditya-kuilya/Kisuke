# Kisuke Site Map

> Complete site structure for the Kisuke marketing website.

---

# Page Hierarchy

```
/                           Homepage (landing)
├── /features              Features overview
├── /architecture          Architecture deep-dive
├── /cli                   CLI documentation
├── /docs                  Documentation hub
├── /docs/getting-started  Getting started guide
├── /docs/domain-model     Domain model overview
├── /docs/resume           Resume engine docs
├── /docs/search           Search engine docs
├── /docs/integrations     Integrations docs
├── /docs/ai               AI abstraction docs
├── /blog                  Blog (future)
├── /changelog             Changelog
├── /github                GitHub repository (external)
└── /security              Security policy
```

---

# Navigation Structure

## Primary Nav (Header)

| Label | Route | Notes |
|-------|-------|-------|
| Kisuke | `/` | Wordmark, left-aligned |
| Features | `/features` | |
| Docs | `/docs` | |
| CLI | `/cli` | |
| Changelog | `/changelog` | |
| GitHub | `https://github.com/...` | External link, icon |
| Star on GitHub | `https://github.com/...` | CTA button, external |

## Footer

| Column | Links |
|--------|-------|
| Product | Features, Architecture, CLI, Changelog |
| Docs | Getting Started, Domain Model, Resume, Search, Integrations, AI |
| Community | GitHub, Contributing, Code of Conduct |
| Legal | License (MIT), Security |

---

# Page Purpose

## `/` — Homepage

The single most important page. Conveys:

1. What Kisuke is (one sentence)
2. Why it exists (one paragraph)
3. How it works (architecture diagram)
4. What it looks like (CLI demo)
5. How to get it (install command)

Target: developer who has 30 seconds.

## `/features` — Features

Detailed feature breakdown with terminal screenshots and Markdown examples:

- Context reconstruction
- Markdown-native storage
- Local-first operation
- Search engine
- Review system
- AI abstraction
- Plugin system
- Integrations

## `/architecture` — Architecture

Visual deep-dive into the layered architecture:

- Component diagram
- Domain model visualization
- Data flow
- Dependency rules

## `/cli` — CLI Documentation

Full CLI reference:

- Command list
- Usage examples
- JSON output mode
- Configuration

## `/docs` — Documentation Hub

Entry point to all documentation with card-based navigation.

## `/changelog` — Changelog

Version history in a clean, scannable format.

---

# SEO Strategy

## Title Tags

| Page | Title |
|------|-------|
| `/` | Kisuke — Local-first context reconstruction |
| `/features` | Features — Kisuke |
| `/architecture` | Architecture — Kisuke |
| `/cli` | CLI — Kisuke |
| `/docs` | Documentation — Kisuke |
| `/changelog` | Changelog — Kisuke |

## Meta Descriptions

| Page | Description |
|------|-------------|
| `/` | Resume any project in seconds. Kisuke reconstructs working context from Markdown files. Local-first, offline-ready, no cloud required. |
| `/features` | Markdown-native storage, instant search, context reconstruction, AI abstraction, and plugin system. |
| `/architecture` | Clean Architecture, single ownership, Markdown as source of truth. See how Kisuke is built. |

## Open Graph

- Image: `/og-image.png` (1200x630)
- Type: website
- Locale: en_US

---

# URL Conventions

- All lowercase
- Hyphens for separators
- No trailing slashes
- No file extensions
- Canonical URLs with `rel="canonical"`

---

# Performance Targets

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.0s |
| Largest Contentful Paint | < 1.5s |
| Cumulative Layout Shift | < 0.05 |
| Time to Interactive | < 1.5s |
| Total page weight | < 100KB (excluding images) |

---

# Implementation Priority

1. Homepage (`/`) — Phase 1
2. Features (`/features`) — Phase 2
3. CLI (`/cli`) — Phase 2
4. Docs hub (`/docs`) — Phase 3
5. Architecture (`/architecture`) — Phase 3
6. Changelog (`/changelog`) — Phase 3
