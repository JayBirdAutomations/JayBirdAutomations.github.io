# 08 — Custom AI Dashboards

**Price:** Enterprise only. Start at $7,500 setup + $499/mo hosting. · **Timeline:** 2–4 weeks

## What this is

A live web dashboard that pulls business data from multiple sources, applies AI analysis, and shows the operator what to do — not just what happened.

Typical use cases:
- Auto repair: jobs in progress, parts on order, customers due for follow-up, tech utilization
- Law firm: cases in pipeline, billable-hour status, client touchpoints due, at-risk matters
- Restaurant: covers vs forecast, inventory alerts, review trends, staff schedule gaps

## Intake questions

1. What decisions do you make daily/weekly? What data do you need to make them well?
2. Where is your data today? (List every system: POS, CRM, accounting, spreadsheets, email…)
3. Who needs to see the dashboard? Just you? Team? External stakeholders?
4. How fresh does data need to be? (Real-time, hourly, daily?)
5. What's the "holy shit" insight you've never been able to see but always wanted?

## Delivery steps

1. **Discovery sprint (week 1):** Audit every data source. Define KPIs. Sketch wireframes. Deliver a scope doc + mockup to client for sign-off BEFORE building.
2. **Data pipeline (week 1–2):** n8n or Python jobs to pull data from each source into a central store (Postgres/Supabase/Airtable — pick based on client comfort).
3. **AI layer (week 2–3):** Claude-powered summaries, anomaly detection, recommendations. Not "chatbot in a dashboard" — pre-computed insights that appear as cards.
4. **UI (week 2–3):** Next.js or plain HTML + Chart.js. Hosted on Vercel. Auth via Clerk or magic-link email.
5. **Deploy + test (week 4):** Private URL, client logs in, validates numbers against their gut.
6. **Handoff training:** 1-hour call + Loom walkthrough.

## Tech stack defaults

| Layer | Tool |
|---|---|
| Data pulls | n8n |
| Store | Supabase (Postgres) |
| Backend | Cloudflare Workers or Vercel Functions |
| AI | Anthropic Claude API |
| Frontend | Next.js + Tailwind + Chart.js |
| Auth | Clerk |
| Hosting | Vercel |

## Deliverables checklist

- [ ] Signed scope doc with KPI definitions
- [ ] Live dashboard URL with auth
- [ ] Data refreshing on schedule (verify for 7 days before sign-off)
- [ ] Source code in client-accessible repo OR escrow agreement
- [ ] Admin trained
- [ ] 30-day bug-fix guarantee included

## Pricing ladder

- **$7,500 + $499/mo** — 1 data source, 5 KPIs, single user
- **$12,500 + $799/mo** — 3 data sources, 10 KPIs, up to 5 users, 1 AI-insight module
- **$25,000 + $1,499/mo** — custom scope, multi-user, multiple AI modules, SSO

## Sell this carefully

Don't pitch this to sub-$1M-revenue businesses — they don't have the data maturity. Best fit: businesses that already have a CRM + accounting + one operational system, and use them.
