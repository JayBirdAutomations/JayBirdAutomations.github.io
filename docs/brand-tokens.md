# Jaybird Brand Tokens — "Aurora Circuit"

Phase 3 rebrand reference. Single source of truth for colors, typography, and motion used by the Jaybird Automations site and the reusable Premium Agency Template.

---

## Palette

| Token | Hex | Usage |
|---|---|---|
| `--bg-0` | `#05060a` | Page background (deepest black) |
| `--bg-1` | `#0b0d14` | Card background |
| `--bg-2` | `#141826` | Elevated surfaces, mega menu panel |
| `--signal` | `#c6f24e` | **Signature accent** — primary CTAs, highlighted words, video glow |
| `--signal-dim` | `#8fb22f` | Hover states, subdued signal |
| `--ember` | `#ffb347` | Secondary accent (replaces old gold) — pricing highlights, badges |
| `--text` | `#ecedf0` | Primary text |
| `--text-dim` | `#9aa0ad` | Secondary / muted text |
| `--text-faint` | `#5a6070` | Tertiary / captions |
| `--line` | `rgba(255,255,255,0.08)` | Default hairline borders |
| `--line-hot` | `rgba(198,242,78,0.35)` | Signal-tinted borders (active states) |
| `--glass` | `rgba(20,24,38,0.55)` | Backdrop for glass-morphism pill nav |

### Swatches (render in VS Code / GitHub preview)

- 🟩 `#c6f24e` — **Signal** (signature accent)
- 🟧 `#ffb347` — Ember (secondary accent)
- ⬛ `#05060a` — Background base
- ⬜ `#ecedf0` — Text

### Why this palette

- **Lime-chartreuse signal** is recognizable — the way Vercel owns pink or Linear owns purple. Distinct from competitors, easy to spot in screenshots.
- **Near-black base** reads as "engineered / hardware" rather than generic dark SaaS.
- **Ember amber** replaces gold — warmer, less casino, more premium.
- **Deprecates:** old `--accent #6c63ff` (purple), `--accent2 #00d4ff` (cyan), `--gold #ffd700` — these disappear entirely in Phase 3B.

---

## Typography

Loaded via Google Fonts (add to `<head>` in Phase 3B):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

| Role | Family | Weights | Where |
|---|---|---|---|
| Display / H1–H3 | **Space Grotesk** | 500, 600, 700 | Hero, section headings, nav logo |
| Body / UI | **Inter** | 400, 500, 600 | Paragraphs, buttons, forms, cards |
| Mono (future) | JetBrains Mono | 400, 500 | Code, stats, technical callouts (Phase 3C) |

### Type scale

```css
--fs-hero:    clamp(2.75rem, 7vw, 5.5rem);   /* 44px → 88px */
--fs-h1:      clamp(2rem, 4.5vw, 3.25rem);   /* 32px → 52px */
--fs-h2:      clamp(1.5rem, 3vw, 2.25rem);   /* 24px → 36px */
--fs-h3:      1.25rem;                       /* 20px */
--fs-body:    1rem;                          /* 16px */
--fs-small:   0.875rem;                      /* 14px */
--fs-tiny:    0.75rem;                       /* 12px (labels, badges) */

--lh-tight:   1.1;
--lh-normal:  1.55;
--lh-loose:   1.75;

--tracking-tight: -0.02em;   /* headings */
--tracking-wide:  0.15em;    /* uppercase labels */
```

---

## Motion principles

1. **Scroll-driven, not time-driven.** Every scene transition tied to scroll progress via GSAP ScrollTrigger. User controls pacing.
2. **Ease with intent.** Default easing: `power2.out` for reveals, `power3.inOut` for scrubbed video. No bouncy springs.
3. **Respect reduced motion.** Wrap all GSAP animations behind `matchMedia('(prefers-reduced-motion: no-preference)')`.
4. **Never animate more than 3 things at once** in the viewport. Cognitive overload = cheap.

---

## Radius, spacing, shadows

```css
--radius-sm:  8px;
--radius-md:  14px;
--radius-lg:  22px;
--radius-pill: 999px;     /* glass nav */

--gap-xs: 8px;
--gap-sm: 16px;
--gap-md: 24px;
--gap-lg: 40px;
--gap-xl: 80px;

--shadow-glow:     0 0 40px rgba(198,242,78,0.25);
--shadow-lift:     0 12px 40px rgba(0,0,0,0.5);
--shadow-card:     0 2px 12px rgba(0,0,0,0.35);
```

---

## File status

- **Phase 3A** — this doc committed, `/assets/video` + `/assets/img` scaffolded, `index.html` untouched
- **Phase 3B** — tokens move into `index.html` `:root`, fonts loaded, GSAP integrated
