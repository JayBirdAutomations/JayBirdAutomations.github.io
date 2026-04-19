# Jaybird Automations — Playbook

**Start here every time.** This is the single index for running the business.

---

## When someone responds to outreach / books a call

Open `sales/discovery-call-script.md` → run the call → send `sales/proposal-template.md`.

## When someone says YES

1. Open `ops/onboarding-runbook.md` — follow it top to bottom.
2. Copy `clients/_template/` → rename to `clients/<client-slug>/`.
3. Fill in `00-brief.md` and `01-scope-and-contract.md`.
4. Send contract + invoice for 50% deposit.
5. Once deposit clears, open the matching `services/XX-*/delivery-runbook.md` and start building.

## When doing monthly retainer work

Open `ops/weekly-retainer-checklist.md` → work the checklist → log into the client folder.

## When delivering / wrapping a project

Open `ops/handoff-checklist.md` → send final invoice → archive client folder.

---

## Where everything lives

| What | Folder | Use when |
|---|---|---|
| **Root playbook** | `JAYBIRD-PLAYBOOK.md` (this file) | Always start here |
| **Active client work** | `clients/<slug>/` | Per-client briefs, scope, deliverables, invoices |
| **Service delivery guides** | `services/` | Building anything for a client |
| **Sales materials** | `sales/` | Pre-signature: proposals, contracts, pricing |
| **Business ops** | `ops/` | Onboarding, handoff, credentials, retainers |
| **Brand + design tokens** | `docs/brand-tokens.md` | Client brand setup |
| **Phase 3 roadmap** | `docs/phase3-roadmap.md` | Internal site roadmap |
| **Live website** | `index.html` + `assets/` + `blog/` + `chatbot/` | Production site |
| **Lead gen tools** | `tools/*.py` | Internal prospecting (not client-facing) |

---

## The 8 services (matches pricing tiers)

| # | Service | Tier | Delivery guide |
|---|---|---|---|
| 01 | Quick Launch Website | $1,499 | `services/01-quick-launch-website/` |
| 02 | Business Build (site + chatbot + blog) | $3,999 | `services/02-business-build/` |
| 03 | Growth Retainer (monthly) | $4,999/mo | `services/03-growth-retainer/` |
| 04 | AI Chatbot (standalone add-on) | $500–$1,500 | `services/04-ai-chatbot/` |
| 05 | AI Blog Engine | $1,500 setup + retainer | `services/05-ai-blog-engine/` |
| 06 | N8N Workflow Automation | hourly or scoped | `services/06-n8n-automation/` |
| 07 | AI Commercials | $1,499 per spot | `services/07-ai-commercials/` |
| 08 | Custom AI Dashboards | Enterprise | `services/08-custom-ai-dashboards/` |

Each service folder has a `delivery-runbook.md` — the exact steps, files, and checklists.

---

## Emergency contacts / credentials

**Never put real credentials in git.** All per-client secrets go in `clients/<slug>/02-credentials.md` — that file is gitignored by pattern.

See `ops/credentials-policy.md` for the rule.

---

## House rules

- Every client gets their own folder. No exceptions.
- 50% deposit before any work starts.
- Contract signed before deposit invoice sent.
- Every delivery ends with `ops/handoff-checklist.md` run.
- Testimonial + case study ask is step 1 of handoff — don't skip.
