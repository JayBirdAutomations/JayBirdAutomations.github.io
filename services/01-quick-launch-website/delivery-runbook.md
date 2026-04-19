# 01 — Quick Launch Website

**Price:** $1,499 flat · **Timeline:** 5–7 days · **Deposit:** $750 (50%)

## What's included

- 1-page cinematic site (hero + services + about + contact)
- Aurora Circuit design system (lime/amber palette, Space Grotesk + Inter)
- Mobile responsive
- Basic SEO (meta, schema, sitemap)
- Google Analytics 4 + Search Console setup
- Domain + hosting walkthrough (client owns both)
- 1 round of revisions

## What's NOT included

- Chatbot (add $500 = upgrade to Business Build)
- Blog system (add $1,500 = upgrade to Business Build)
- Custom illustrations/video

## Source files

Clone from `index.html` on main branch. Everything you need is already built:
- Glass-pill navbar pattern
- Aurora Circuit tokens (`--signal: #c6f24e`, `--ember: #ffb347`)
- Body ambient drift layer
- Section-based structure

## Delivery steps

1. **Intake** — client fills `sales/intake-form.md`. Review their brand, target audience, must-have sections.
2. **Asset collection** — get logo, brand colors (if they have any), hero copy, service list, contact info.
3. **Branch setup** — in a new repo/folder per client. Never push client work to jaybirdautomations.com repo.
4. **Copy base template** — start from a stripped version of `index.html` (remove sections you don't need).
5. **Apply client brand** — swap tokens in `:root`, swap fonts if needed, swap copy.
6. **Wire contact form** — Formspree, Netlify Forms, or their preferred tool.
7. **SEO pass** — title, meta description, Open Graph image, schema.org LocalBusiness, sitemap.xml, robots.txt.
8. **Analytics** — GA4 tag, Search Console verify.
9. **Staging review** — deploy to Netlify/Vercel preview URL. Send to client.
10. **1 revision round** — batch all feedback into one pass.
11. **Production deploy** — push to their domain. Verify DNS + SSL.
12. **Handoff** — run `ops/handoff-checklist.md`.

## Deliverables checklist

- [ ] Live site on their domain
- [ ] Mobile tested (375px, 768px, 1440px)
- [ ] Lighthouse ≥ 85 desktop, ≥ 70 mobile
- [ ] GA4 live, test event fired
- [ ] Search Console verified, sitemap submitted
- [ ] Client has admin access (Netlify/Vercel, domain registrar, GA, GSC)
- [ ] Written handoff doc (how to edit, who to call)

## Upsells (mention during handoff)

- Chatbot add-on ($500)
- Blog engine ($1,500 setup + $500/mo)
- Monthly retainer for tweaks + SEO content ($499/mo)
