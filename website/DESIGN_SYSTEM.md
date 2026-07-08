# Kisuke Design System

> A dark-mode-first, engineering-first design system for Kisuke's marketing website.
> Blends Linear (80%), Vercel (10%), Claude (7%), and Stripe (3%).
> No flashy animations. No glassmorphism. No neon. No heavy gradients.

---

# Colors

## Palette

Dark mode only. The entire system operates on a single dark surface.

### Surfaces

| Token | Value | Use |
|-------|-------|-----|
| `canvas` | `#0a0a0b` | Page background. The near-black void. |
| `surface` | `#111113` | Cards, panels, elevated containers |
| `surface-raised` | `#18181b` | Hovered cards, active panels |
| `surface-overlay` | `#1f1f23` | Modals, dropdowns, floating elements |
| `surface-inset` | `#08080a` | Code blocks, terminal windows, inset wells |

### Text

| Token | Value | Use |
|-------|-------|-----|
| `text-primary` | `#ececef` | Headings, primary text. Soft white, never pure #fff. |
| `text-secondary` | `#a0a0a8` | Body copy, descriptions, nav links |
| `text-tertiary` | `#6b6b73` | Captions, metadata, timestamps |
| `text-disabled` | `#45454d` | Placeholders, disabled labels |

### Borders

| Token | Value | Use |
|-------|-------|-----|
| `border-subtle` | `#ffffff0d` | 1px card borders, dividers. Near-invisible. |
| `border-default` | `#ffffff1a` | Stronger structural borders when needed |
| `border-focus` | `#6366f1` | Focus rings, active indicators |

### Accent

| Token | Value | Use |
|-------|-------|-----|
| `accent` | `#6366f1` | Primary accent. Indigo-violet. Links, focus, active states. |
| `accent-hover` | `#818cf8` | Hovered accent elements |
| `accent-muted` | `#6366f110` | Accent tint for subtle backgrounds |
| `accent-strong` | `#4f46e5` | Pressed accent elements |

### Code Syntax

| Token | Value | Use |
|-------|-------|-----|
| `code-keyword` | `#c084fc` | Keywords, imports |
| `code-string` | `#86efac` | Strings, literals |
| `code-comment` | `#6b6b73` | Comments |
| `code-function` | `#93c5fd` | Function names |
| `code-type` | `#fbbf24` | Types, classes |
| `code-operator` | `#a0a0a8` | Operators, punctuation |
| `code-number` | `#f9a8d4` | Numbers |

### Semantic

| Token | Value | Use |
|-------|-------|-----|
| `success` | `#22c55e` | Success states |
| `warning` | `#f59e0b` | Warning states |
| `error` | `#ef4444` | Error states |

---

# Typography

## Font Family

| Role | Font | Fallback |
|------|------|----------|
| Display / Headings | Inter | -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Body | Inter | same fallback |
| Code / Terminal | JetBrains Mono | "Fira Code", "Cascadia Code", monospace |

Inter at weight 510 for headings (Linear's signature). JetBrains Mono for all code.

## Scale

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| `display-xl` | 56px | 510 | 1.05 | -1.68px | Hero headline |
| `display-lg` | 40px | 510 | 1.1 | -1.2px | Section headline |
| `display-md` | 28px | 510 | 1.15 | -0.56px | Sub-section headline |
| `display-sm` | 22px | 510 | 1.2 | -0.44px | Card title |
| `body-lg` | 17px | 400 | 1.6 | 0 | Lead paragraph |
| `body-md` | 15px | 400 | 1.6 | 0 | Default body |
| `body-sm` | 13px | 400 | 1.5 | 0 | Captions, metadata |
| `caption` | 11px | 500 | 1.4 | 0.5px | Uppercase eyebrows |
| `code` | 14px | 400 | 1.6 | 0 | Code blocks |
| `code-sm` | 12px | 400 | 1.5 | 0 | Inline code |

## Principles

- Headings use weight 510 (Inter's distinctive semi-bold). Not 600, not 700.
- Negative letter-spacing on display sizes is mandatory: -1.68px at 56px, scaling proportionally.
- Body text sits at weight 400 with neutral spacing.
- The `caption` token uses uppercase tracking (0.5px) for section eyebrows.
- There is no italic anywhere. No light weight. No black weight. Weight range is 400–510.
- Code always uses JetBrains Mono. Never substitute.

---

# Spacing

## Base Unit

4px. All spacing is a multiple of 4.

## Scale

| Token | Value | Use |
|-------|-------|-----|
| `space-1` | 4px | Tightest gap |
| `space-2` | 8px | Compact gap |
| `space-3` | 12px | Small gap |
| `space-4` | 16px | Default gap |
| `space-5` | 20px | Medium gap |
| `space-6` | 24px | Card internal padding |
| `space-8` | 32px | Section internal padding |
| `space-10` | 40px | Large gap |
| `space-12` | 48px | Section spacing (compact) |
| `space-16` | 64px | Major section spacing |
| `space-20` | 80px | Hero vertical padding |
| `space-24` | 96px | Full section vertical rhythm |

## Principles

- Card internal padding: `space-6` (24px) to `space-8` (32px).
- Section vertical rhythm: `space-16` (64px) to `space-24` (96px).
- Grid gutters: `space-4` (16px) to `space-6` (24px).
- Inline element spacing: `space-2` (8px) to `space-3` (12px).

---

# Radius

| Token | Value | Use |
|-------|-------|-----|
| `radius-none` | 0 | Full-bleed bands, dividers |
| `radius-sm` | 4px | Inputs, inline code |
| `radius-md` | 6px | Small buttons, tags |
| `radius-lg` | 8px | Feature cards, code blocks |
| `radius-xl` | 12px | Large cards, panels |
| `radius-full` | 9999px | Pills, badges, circular elements |

## Principles

- Cards use `radius-lg` (8px). Not 12px, not 16px. Disciplined.
- Buttons use `radius-full` (pill shape) for CTAs, `radius-md` for app-style buttons.
- Code blocks use `radius-lg` (8px).
- No rounded corners above 12px except pills. The system is architectural, not bubbly.

---

# Shadows

Minimal. The dark palette makes heavy shadows redundant.

| Token | Value | Use |
|-------|-------|-----|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.4)` | Subtle lift on hover |
| `shadow-md` | `0 2px 8px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3)` | Cards, panels |
| `shadow-lg` | `0 4px 16px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.3)` | Floating elements |
| `shadow-glow` | `0 0 20px rgba(99,102,241,0.15)` | Accent glow on focus/active |

## Principles

- Default state: no shadow. Just a 1px `border-subtle`.
- Hover state: `shadow-sm` + `border-default`.
- The accent glow is used sparingly — only on primary CTA hover and active terminal cursor.
- Shadows are low-alpha on dark surfaces. They add texture, not drama.

---

# Motion

Restrained. Linear-inspired: functional, not decorative.

## Duration

| Token | Value | Use |
|-------|-------|-----|
| `duration-instant` | 0ms | Immediate feedback |
| `duration-fast` | 100ms | Hover states, focus rings |
| `duration-normal` | 200ms | Transitions, reveals |
| `duration-slow` | 300ms | Page-level transitions |
| `duration-slower` | 500ms | Complex orchestration (rare) |

## Easing

| Token | Value | Use |
|-------|-------|-----|
| `ease-default` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Standard transitions |
| `ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Elements entering |
| `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Bidirectional |

## Principles

- Hover transitions: 100ms. Instant feel.
- Card hover: `duration-fast`, `ease-default`. Border brightens, shadow appears.
- Scroll reveals: `duration-slow`, `ease-out`. Fade up 8px. One direction only.
- No bounce. No spring. No elastic. No rotation. No scale.
- No entrance animations on page load. Content appears immediately.
- Stagger delays for sequential reveals: max 50ms between items, max 300ms total.

---

# Components

## Navigation

### Nav Bar

Fixed top. `canvas` background. `border-subtle` bottom border.

- Height: 56px
- Max-width: 1200px centered
- Left: Wordmark (text, not SVG logo)
- Center: Nav links (4 max)
- Right: CTA button

### Nav Link

- Font: `body-md` (15px / 400)
- Color: `text-secondary`
- Hover: `text-primary`
- Padding: `space-2` `space-3`
- No underline, no decoration

## Buttons

### Button Primary (CTA)

- Background: `accent` (#6366f1)
- Text: `#ffffff`
- Font: `body-md` (15px / 500)
- Padding: `space-2` `space-5` (8px 20px)
- Height: 40px
- Radius: `radius-full` (pill)
- Hover: `accent-hover`, `shadow-glow`

### Button Secondary

- Background: transparent
- Text: `text-primary`
- Border: 1px `border-default`
- Font: `body-md` (15px / 500)
- Padding: `space-2` `space-5`
- Height: 40px
- Radius: `radius-full`
- Hover: `surface-raised`, `border-default`

### Button Ghost

- Background: transparent
- Text: `text-secondary`
- Font: `body-md` (15px / 500)
- Padding: `space-2` `space-3`
- Height: 36px
- Radius: `radius-md`
- Hover: `surface-raised`, `text-primary`

## Cards

### Feature Card

- Background: `surface`
- Border: 1px `border-subtle`
- Radius: `radius-lg` (8px)
- Padding: `space-6` (24px)
- Hover: `surface-raised`, `border-default`, `shadow-sm`

### Code Card

- Background: `surface-inset`
- Border: 1px `border-subtle`
- Radius: `radius-lg` (8px)
- Padding: `space-4` (16px)
- Font: `code` (14px / JetBrains Mono)
- No hover state

### Terminal Card

- Background: `surface-inset`
- Border: 1px `border-subtle`
- Radius: `radius-lg` (8px)
- Header: 32px bar with dot indicators (red, yellow, green — muted)
- Body: `code` font, scrollable

## Badges / Tags

- Background: `accent-muted`
- Text: `accent`
- Font: `caption` (11px / 500 / uppercase)
- Padding: `space-1` `space-3`
- Radius: `radius-full`

## Section Eyebrow

- Font: `caption` (11px / 500 / uppercase)
- Color: `accent`
- Letter-spacing: 0.5px
- Margin-bottom: `space-3`

---

# Grid

## Container

| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| Mobile (< 640px) | 100% | `space-4` (16px) |
| Tablet (640–1024px) | 100% | `space-6` (24px) |
| Desktop (> 1024px) | 1200px | `space-8` (32px) |

## Column System

12-column grid. No framework. CSS Grid only.

| Context | Columns | Gap |
|---------|---------|-----|
| Feature grid (desktop) | 3 | `space-4` (16px) |
| Feature grid (tablet) | 2 | `space-4` |
| Feature grid (mobile) | 1 | `space-4` |
| Hero | 2 (6/6 split) or 1 (mobile) | `space-8` |
| CLI demo | 1 (full width) | — |

## Section Rhythm

Every section follows the same vertical pattern:

```
Section {
  padding-top: space-24 (96px)
  padding-bottom: space-24 (96px)
}
```

Mobile: `space-16` (64px) top/bottom.

---

# Accessibility

## Requirements

- All text meets WCAG AA contrast (4.5:1 for body, 3:1 for large text).
- `text-primary` (#ececef) on `canvas` (#0a0a0b): contrast ratio ~15.5:1.
- `text-secondary` (#a0a0a8) on `canvas` (#0a0a0b): contrast ratio ~7.2:1.
- `accent` (#6366f1) on `canvas` (#0a0a0b): contrast ratio ~4.6:1.
- Focus rings: 2px `border-focus` offset 2px. Always visible on keyboard focus.
- Touch targets: minimum 44x44px for interactive elements.
- All images have meaningful `alt` text.
- Semantic HTML: `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`.
- Skip-to-content link as first focusable element.
- Reduced motion: respect `prefers-reduced-motion` by disabling scroll reveals.
- Screen reader: all decorative elements use `aria-hidden="true"`.

## Keyboard Navigation

- Tab order follows visual layout.
- No keyboard traps.
- Escape closes any overlay.
- Arrow keys navigate within component groups.

---

# Do's and Don'ts

## Do

- Use near-black canvas with soft-white text. The contrast is the brand.
- Keep borders near-invisible (`border-subtle`). The structure is implied, not drawn.
- Use accent color sparingly — one CTA per section, links, focus rings.
- Set display type in Inter 510 with negative tracking.
- Keep code in JetBrains Mono. Always.
- Use the 4px spacing grid religiously.
- Let whitespace do the work.

## Don't

- Don't use pure white (#ffffff) for text. The brand is soft white (#ececef).
- Don't add gradients anywhere. The brand is flat.
- Don't use glassmorphism, blur, or frosted effects.
- Don't add neon glows or saturated color backgrounds.
- Don't animate on page load. Content appears instantly.
- Don't use bounce, spring, or elastic easing.
- Don't add decorative illustrations. Use real product screenshots and diagrams.
- Don't use more than one accent color.
- Don't round cards above 8px. The system is architectural.
