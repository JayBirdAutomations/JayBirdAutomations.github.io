# Phase 3 Roadmap — Cinematic Site Transformation

Transform jaybirdautomations.com into a Terminal Industries–caliber showcase, and extract the result as a reusable **Premium Agency Template** for $10k–25k client engagements.

All Phase 3 work lives on branch `phase3-redesign`. `main` (production) is untouched until 3D merges back.

---

## 3A — Foundation & Rebrand ✅ (current)

Scaffolding only. No visible change to the live site.

- [x] Branch `phase3-redesign` created
- [x] `/assets/video/` and `/assets/img/` folders scaffolded
- [x] `/docs/brand-tokens.md` — "Aurora Circuit" palette + Space Grotesk / Inter typography
- [x] `/docs/phase3-roadmap.md` (this file)
- [ ] Jay generates 5 AI video loops (see brand-tokens + video brief)
- [ ] Jay approves palette (or requests swap)

**Ship criteria:** Scaffolding merged onto branch, palette approved, video clips delivered.

---

## 3B — Core Motion System

First visible redesign. One production-quality section to prove the direction before doing the rest.

- [ ] Load GSAP 3.12 + ScrollTrigger via CDN
- [ ] Load Google Fonts (Space Grotesk + Inter)
- [ ] Swap `:root` tokens to Aurora Circuit palette
- [ ] Glass-morphism pill navbar with `backdrop-filter: blur()`
- [ ] Hero: scroll-scrubbed video (`hero-circuit.mp4`), large Space Grotesk H1, signal-lime CTA
- [ ] Redesign **Services** section with scroll-reveal cards + hover tilt (Vanilla Tilt)
- [ ] `prefers-reduced-motion` fallback for everything
- [ ] Mobile: nav collapses cleanly, videos use poster images on small screens
- [ ] Lighthouse: Performance ≥ 85 on desktop, ≥ 70 mobile

**Ship criteria:** Nav + hero + services all live on the staging branch, look like Terminal, and don't blow up mobile.

---

## 3C — Mega Menu & Full Section Pass

Finish every section to 3B quality.

- [ ] **Resources mega menu** — full-width panel on hover, sidebar with 5–8 categories + thumbnail preview grid (Blog, Case Studies, Videos, Webinars, Tools, Calculator, etc.)
- [ ] Commercials section — scroll-scrubbed `commercial-studio.mp4` with captions that pin & advance
- [ ] N8N Workflows section — `n8n-nodes.mp4` with floating node graphics
- [ ] AI Agents section — `agents-working.mp4`, quote-style testimonial card
- [ ] Lead Gen section — `leadgen-map.mp4` with animated Las Vegas stat counters
- [ ] Pricing — interactive tier cards, annual/monthly toggle, hover-lift
- [ ] Contact — cinematic fade-in, updated form styling
- [ ] FAQ — accordion with smoother transitions
- [ ] Footer — 3-col dark with signal-lime hairlines
- [ ] Full mobile polish pass

**Ship criteria:** Full site on `phase3-redesign` branch matches Terminal quality end-to-end.

---

## 3D — Launch + Premium Agency Template

- [ ] QA pass: Lighthouse, broken link check, SEO/AIO verification (Schema.org, sitemap, llms.txt still accurate)
- [ ] Merge `phase3-redesign` → `main` → live on jaybirdautomations.com
- [ ] Extract the build as a Claude skill: **"Premium Agency Template"**
  - Reusable tokens doc, GSAP scaffold, mega-menu component, video-scene system
  - Parameterized for client brand (colors, fonts, copy, 5 video slots)
- [ ] Create a client-facing landing page positioning the template at $10k–25k
- [ ] Add a "Built with Jaybird Premium Template" badge option
- [ ] First client pilot (identify candidate from 650-lead database)

**Ship criteria:** Live on main, template skill exists, first client pitch deck ready.

---

## Timeline estimate

| Phase | Effort | Calendar (realistic, Jay's pace) |
|---|---|---|
| 3A | 1–2 sessions | This week |
| 3B | 3–5 sessions | Next 1–2 weeks |
| 3C | 5–8 sessions | Following 2–3 weeks |
| 3D | 2–3 sessions | Final week |
| **Total** | ~2 months part-time | |

Shortens significantly if Jay batches video generation early (the only blocking dependency).
