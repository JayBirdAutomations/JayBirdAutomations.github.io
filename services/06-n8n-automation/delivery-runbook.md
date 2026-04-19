# 06 — N8N Workflow Automation

**Price:** Scoped per project. Common: $500 (simple), $1,500 (integrated), $3,000+ (multi-system).

## What this is

Custom automation workflows built in n8n. Typical jobs:
- Lead capture → CRM sync
- Email/SMS follow-up sequences
- Document processing (invoices, contracts, intake forms)
- Cross-platform sync (Google Sheets ↔ Airtable ↔ HubSpot)
- Scheduled reports
- API integrations (the client needs X + Y to talk but they don't)

## Intake questions

1. What's the manual process today? (Walk me through it step by step.)
2. Where does the data come IN? (Form, email, upload, webhook, API?)
3. Where does it need to GO? (CRM, spreadsheet, email, another system?)
4. How often? (Real-time, daily, weekly?)
5. What happens when it fails? (Retry, email Jay, alert client?)
6. Who owns the accounts/API keys?

## Delivery steps

1. **Scope doc** — before pricing, write the workflow in plain English in `clients/<slug>/01-scope-and-contract.md`. Client signs off on that description.
2. **Build in dev n8n instance first** — never build live. Use test data.
3. **Document every node** — add notes in n8n + screenshot the final graph.
4. **Error handling** — every workflow needs: retry policy, error notification to Jay + client, dead-letter for bad records.
5. **Credentials** — client enters their own API keys during handoff OR they stay in Jay's n8n (agreed up front — pricing differs).
6. **Export + save** — export JSON to `clients/<slug>/04-deliverables/workflow-<name>.json`.
7. **Test run** — with real (non-destructive) data. Client watches.
8. **Activate** — flip the toggle. Monitor for 48hrs.
9. **Handoff** — Loom video of the graph + how to pause + who to call if it breaks.

## Deliverables checklist

- [ ] Workflow JSON saved to client folder
- [ ] Screenshot of the graph saved
- [ ] Loom walkthrough (< 5 min)
- [ ] 48-hour monitoring period complete
- [ ] Error alerts verified (intentionally break it once)
- [ ] Client has access to n8n instance (or agreed to Jay-hosted)

## Pricing ballpark

| Scope | Price |
|---|---|
| Single trigger + 1–3 nodes (e.g. form → email) | $500 |
| Multi-step with 1 integration (e.g. Typeform → HubSpot + Slack) | $1,500 |
| Cross-system sync, data transforms, conditional logic | $3,000+ |
| Complex multi-workflow system | $5,000+ scoped |

## Jay-hosted vs client-hosted

**Jay-hosted:** +$49/mo. Jay's n8n, Jay's credentials, Jay maintains. Client gets results, not the workflow itself.

**Client-hosted:** Client owns n8n cloud or self-hosted. Jay delivers the JSON. Client owns forever. Higher upfront friction but no monthly.
