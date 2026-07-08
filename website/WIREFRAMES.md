# Kisuke Wireframes

> Homepage wireframes for the Kisuke marketing website.
> Dark mode only. No placeholder text. Real content throughout.

---

# Homepage Wireframe

## Layout Structure

```
┌─────────────────────────────────────────────────────┐
│ NAV BAR (fixed, 56px)                               │
│ [Kisuke]  Features  Docs  CLI  Changelog  [GitHub]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│ HERO (96px vertical padding)                        │
│                                                     │
│ ┌─────────────────────┐  ┌─────────────────────┐   │
│ │                     │  │                     │   │
│ │  Resume any         │  │  Terminal window    │   │
│ │  project in         │  │  showing `kisuke    │   │
│ │  seconds.           │  │  resume` output     │   │
│ │                     │  │                     │   │
│ │  One sentence.      │  │  [kisuke resume]    │   │
│ │  One paragraph.     │  │  Project: Build     │   │
│ │                     │  │  Kisuke             │   │
│ │  [Install] [GitHub] │  │  Next: Implement    │   │
│ │                     │  │  CLI commands       │   │
│ │  pip install kisuke │  │                     │   │
│ │                     │  └─────────────────────┘   │
│ └─────────────────────┘                            │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ FEATURES (96px vertical padding)                    │
│                                                     │
│ EYEBROW: CAPABILITIES                               │
│                                                     │
│ What Kisuke does                                     │
│                                                     │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│ │ Context  │ │ Markdown │ │ Local    │            │
│ │ Recon-   │ │ Native   │ │ First    │            │
│ │ struct   │ │ Storage  │ │          │            │
│ │          │ │          │ │          │            │
│ │ Resume   │ │ Every    │ │ Works    │            │
│ │ any      │ │ entity   │ │ offline. │            │
│ │ project  │ │ stored   │ │ No       │            │
│ │ in       │ │ as .md   │ │ cloud    │            │
│ │ seconds. │ │ files.   │ │ required.│            │
│ └──────────┘ └──────────┘ └──────────┘            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│ │ Search   │ │ Review   │ │ AI       │            │
│ │ Engine   │ │ System   │ │ Optional │            │
│ │          │ │          │ │          │            │
│ │ Fast     │ │ Morning, │ │ Provider │            │
│ │ local    │ │ weekly,  │ │ in-      │            │
│ │ search   │ │ monthly, │ │ dependent│            │
│ │ across   │ │ quarterly│ │ AI layer.│            │
│ │ all      │ │ reviews. │ │          │            │
│ │ entities.│ │          │ │          │            │
│ └──────────┘ └──────────┘ └──────────┘            │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ARCHITECTURE (96px vertical padding)                │
│                                                     │
│ EYEBROW: ARCHITECTURE                               │
│                                                     │
│ Built on solid foundations                           │
│                                                     │
│ ┌─────────────────────────────────────────────────┐│
│ │                                                 ││
│ │  [Component diagram showing layered             ││
│ │   architecture: CLI → Application → Domain      ││
│ │   → Infrastructure → Storage/Search]            ││
│ │                                                 ││
│ │  Clean Architecture.                            ││
│ │  Single ownership.                              ││
│ │  Markdown as source of truth.                   ││
│ │                                                 ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
│ ┌──────────────────┐ ┌──────────────────┐          │
│ │ Domain Model     │ │ Data Flow        │          │
│ │                  │ │                  │          │
│ │ [Entity          │ │ Markdown →       │          │
│ │  relationship    │ │ Parser →         │          │
│ │  diagram]        │ │ Domain →         │          │
│ │                  │ │ Search Index →   │          │
│ │ Mission →        │ │ Resume →         │          │
│ │  Project →       │ │ Context Bundle   │          │
│ │  Task            │ │                  │          │
│ └──────────────────┘ └──────────────────┘          │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ CLI DEMO (96px vertical padding)                    │
│                                                     │
│ EYEBROW: CLI                                        │
│                                                     │
│ Keyboard-first interface                             │
│                                                     │
│ ┌─────────────────────────────────────────────────┐│
│ │ ┌─────────────────────────────────────────────┐ ││
│ │ │ ● ● ●                                       │ ││
│ │ ├─────────────────────────────────────────────┤ ││
│ │ │ $ kisuke resume                             │ ││
│ │ │                                             │ ││
│ │ │ Project: Build Kisuke                       │ ││
│ │ │ Status: Active                              │ ││
│ │ │                                             │ ││
│ │ │ Next Action:                                │ ││
│ │ │   Implement CLI commands                    │ ││
│ │ │                                             │ ││
│ │ │ Related:                                    │ ││
│ │ │   - Decision: Use Markdown as storage       │ ││
│ │ │   - Knowledge: Domain model research        │ ││
│ │ │   - Resource: Clean Architecture docs       │ ││
│ │ │                                             │ ││
│ │ └─────────────────────────────────────────────┘ ││
│ │                                                 ││
│ │ 11 commands. JSON output. Shell completion.     ││
│ │                                                 ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ GITHUB CTA (64px vertical padding)                  │
│                                                     │
│ Open source. MIT licensed.                          │
│ Ready to contribute?                                │
│                                                     │
│ [Star on GitHub]  [Read the Docs]                   │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ FOOTER (64px vertical padding)                      │
│                                                     │
│ Kisuke                                              │
│ Local-first context reconstruction.                 │
│                                                     │
│ Product        Docs          Community     Legal    │
│ Features       Getting Started GitHub      License  │
│ Architecture   Domain Model  Contributing  Security │
│ CLI            Resume        Code of Conduct         │
│ Changelog      Search                                 │
│                Integrations                           │
│                AI                                     │
│                                                     │
│ MIT License. Built with care.                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# Section Details

## Hero

**Content:**
- Headline: "Resume any project in seconds."
- Subheadline: "Kisuke reconstructs working context from Markdown files. Local-first, offline-ready, no cloud required."
- Primary CTA: "Install" (pill button, accent color)
- Secondary CTA: "Star on GitHub" (ghost button)
- Install command: `pip install kisuke` (code block, copyable)
- Right side: Terminal window showing `kisuke resume` output with real data

**Layout:** 2-column (6/6). Text left, terminal right. Single column on mobile.

**Visual:** No illustration. The terminal IS the illustration. Real output, real data.

## Features

**Content:** 6 feature cards in a 3x2 grid.

**Cards:**
1. Context Reconstruction — "Resume any project in seconds."
2. Markdown Native — "Every entity stored as .md files."
3. Local First — "Works offline. No cloud required."
4. Search Engine — "Fast local search across all entities."
5. Review System — "Morning, weekly, monthly, quarterly reviews."
6. AI Optional — "Provider-independent AI layer."

**Each card:**
- Icon (Lucide React, monochrome)
- Title (display-sm, text-primary)
- Description (body-md, text-secondary)

**Layout:** 3-column grid. 2-column on tablet. 1-column on mobile.

## Architecture

**Content:**
- Eyebrow: "Architecture"
- Headline: "Built on solid foundations"
- Full-width architecture diagram (the layered component diagram from the repo)
- Two smaller cards below: Domain Model (entity diagram) and Data Flow (pipeline diagram)

**Visual:** The architecture diagram from `architecture/component-diagram.md` rendered as an SVG/HTML diagram. The domain model relationship diagram from the docs. The data flow pipeline.

## CLI Demo

**Content:**
- Eyebrow: "CLI"
- Headline: "Keyboard-first interface"
- Full-width terminal window showing `kisuke resume` with real output
- Three bullet points: "11 commands. JSON output. Shell completion."

**Visual:** A terminal card with real command output. Syntax-highlighted. The terminal IS the demo.

## GitHub CTA

**Content:**
- Headline: "Open source. MIT licensed."
- Subheadline: "Ready to contribute?"
- Two buttons: "Star on GitHub" (primary) and "Read the Docs" (secondary)

**Layout:** Centered text. No illustration.

## Footer

**Content:**
- Wordmark: "Kisuke"
- Tagline: "Local-first context reconstruction."
- Four columns: Product, Docs, Community, Legal
- Bottom: "MIT License. Built with care."

---

# Responsive Behavior

## Mobile (< 640px)

- Hero: single column. Terminal stacks below text.
- Features: single column stack.
- Architecture: diagram scrolls horizontally or scales down.
- CLI demo: full-width terminal, scrollable.
- Nav: hamburger menu.

## Tablet (640–1024px)

- Hero: 2-column.
- Features: 2-column grid.
- Architecture: full-width.
- CLI demo: full-width.

## Desktop (> 1024px)

- All sections at full layout as wireframed above.

---

# Interaction Details

## Scroll Reveals

- Sections fade in from 8px below.
- Duration: 300ms, ease-out.
- Trigger: when section enters viewport (IntersectionObserver, threshold 0.1).
- Stagger: 50ms between cards in a grid.
- Reduced motion: disabled entirely.

## Hover States

- Feature cards: border brightens, shadow appears (100ms).
- Buttons: background shifts, shadow glow on primary (100ms).
- Nav links: color transitions to text-primary (100ms).

## Copy Install Command

- Click on the install command block copies to clipboard.
- Brief "Copied!" confirmation (1s).

---

# Content Guidelines

## Headlines

- One sentence. No more.
- Active voice. Present tense.
- No buzzwords. No superlatives.
- Example: "Resume any project in seconds."

## Descriptions

- One to two sentences max.
- State what it does, not what it is.
- Example: "Works offline. No cloud required." not "Kisuke is a local-first application."

## Terminal Output

- Always real output from the actual CLI.
- Never fabricated.
- Never abbreviated.
- Shows real entity names and relationships.

## Code Examples

- Always syntactically valid.
- Always copy-pasteable.
- Always complete (no `...` or `# etc`).
