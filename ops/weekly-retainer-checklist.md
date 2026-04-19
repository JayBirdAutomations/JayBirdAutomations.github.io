# Weekly Retainer Checklist

For Growth Retainer clients ($4,999/mo). Work each section in its numbered week of the month.

---

## Week 1 — Report + Strategy

- [ ] Pull GA4 data for previous month
- [ ] Pull Search Console data
- [ ] Check chatbot logs (conversation count, lead count, common questions)
- [ ] Count blog posts published + note top performer
- [ ] Write monthly report to `clients/<slug>/reports/YYYY-MM.md` (template in `services/03-growth-retainer/delivery-runbook.md`)
- [ ] Send report + book 30-min strategy call
- [ ] On the call: pick 1–2 priorities for the month

## Week 2 — Content batch

- [ ] Review auto-generated blog posts from last month. Edit any that are weak.
- [ ] If cron is failing, debug the n8n workflow.
- [ ] Add 2–3 manual posts if client has specific topics they wanted covered.
- [ ] Push fresh sitemap.xml with new posts.

## Week 3 — Automation / feature build

- [ ] Work the priority chosen on the Week 1 call.
- [ ] Examples: new workflow, new page, SEO improvement, lead-gen experiment, chatbot KB expansion.
- [ ] Log the build in `clients/<slug>/03-kickoff-notes.md` with a date.

## Week 4 — Chatbot + housekeeping

- [ ] Review 50 most recent chatbot conversations. Note failure modes.
- [ ] Update knowledge base with corrections + new FAQs.
- [ ] Re-deploy Cloudflare worker with updated prompt.
- [ ] Run uptime check on: site, chatbot endpoint, n8n cron, analytics.
- [ ] Confirm next month's invoice is queued for 1st.
- [ ] If it's month 2 of a 3-month term → schedule renewal conversation for week 1 of next month.

---

## Hours tracking

Retainer includes 4 hours of "miscellaneous" dev/edit time. Track here:

`clients/<slug>/reports/YYYY-MM-hours.md`

If you hit 4 hours, tell the client immediately — "I've used the 4 included hours, anything more this month is hourly at $200/hr. Let me know if you want to hold it until next month's block."

Don't eat overage hours silently. That's how you grow to resent the client.
