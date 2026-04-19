# Services

Each service has its own folder with a `delivery-runbook.md` — follow it step by step when building for a client.

**Source files are NOT duplicated here.** The runbooks point to where the real files live in the repo.

---

## Service catalog

| # | Service | Price | Source files | Delivery time |
|---|---|---|---|---|
| 01 | Quick Launch Website | $1,499 | `index.html` template, `assets/` | 5–7 days |
| 02 | Business Build | $3,999 | 01 + `chatbot/` + `blog/` | 10–14 days |
| 03 | Growth Retainer | $4,999/mo | ongoing | monthly |
| 04 | AI Chatbot | $500–$1,500 | `chatbot/chat-widget.js`, `chatbot/chat-widget.css`, `cloudflare-worker/worker.js` | 3–5 days |
| 05 | AI Blog Engine | $1,500 setup + $500/mo | `blog/template.html`, `blog/posts.json`, `workflows/blog-generator.json` | 5 days |
| 06 | N8N Automation | scoped | n8n cloud / self-hosted | varies |
| 07 | AI Commercials | $1,499/spot | Freepik Pikaso, Kling, ElevenLabs | 3–7 days |
| 08 | Custom AI Dashboards | Enterprise | TBD per client | 2–4 weeks |

---

## How to use these runbooks

1. Client pays deposit (see `ops/onboarding-runbook.md`).
2. Open the matching service folder.
3. Follow `delivery-runbook.md` end to end.
4. Log deliverables in `clients/<slug>/04-deliverables/`.
5. Close out with `ops/handoff-checklist.md`.
