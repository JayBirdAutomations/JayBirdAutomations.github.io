# 03 — Growth Retainer

**Price:** $4,999/mo · **Minimum:** 3-month commitment · **Billing:** 1st of month

## What's included (every month)

- 4 new blog posts (AI-generated, Jay-edited)
- Chatbot knowledge base updates
- 1 new automation or workflow improvement
- Monthly performance report (GA4, Search Console, chatbot logs, lead count)
- Up to 4 hours of "miscellaneous" dev/edit time
- Slack/email priority support (< 24hr response M–F)

## What's NOT included

- New site design (scoped separately)
- AI commercials (scoped separately, $1,499 each)
- Emergency after-hours work (hourly, $200/hr)

## Monthly cadence

See `ops/weekly-retainer-checklist.md` — that's the actual week-by-week work.

**High level:**
- Week 1: Monthly report + strategy check-in call (30 min)
- Week 2: Blog content batch (write, edit, publish)
- Week 3: Automation/feature build
- Week 4: Chatbot review + next-month planning

## Onboarding a new retainer client

1. Confirm website + chatbot + blog are already live (if not, they need Business Build first).
2. Get access: GA4, Search Console, domain DNS, hosting, chatbot admin.
3. Schedule first monthly check-in (same day/time every month).
4. Set up Slack channel or shared email thread.
5. Add to `clients/<slug>/` with retainer start date + end date in `01-scope-and-contract.md`.
6. Calendar reminders for: monthly invoice (auto), weekly checklist, quarterly renewal conversation.

## Monthly report template

Save to `clients/<slug>/reports/YYYY-MM.md`:
```
# <Client> — Monthly Report, <Month Year>

## Highlights
- [top win of the month]
- [top metric]

## Traffic (GA4)
- Sessions: X (prev: Y, delta: Z%)
- Top page:
- Top source:

## Search (Search Console)
- Impressions: X
- Clicks: X
- Top query:

## Chatbot
- Conversations: X
- Leads captured: X
- Top question asked:

## Content published
- [post 1 — URL]
- [post 2 — URL]
- [post 3 — URL]
- [post 4 — URL]

## Automation work this month
- [what I built]

## Next month plan
- [1–2 priorities]
```

## Renewal conversation

Have it at month 2 of a 3-month term. Don't let it lapse without a call.
