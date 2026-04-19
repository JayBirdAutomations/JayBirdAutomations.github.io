# Onboarding Runbook — "They Said Yes"

Follow top to bottom. Every client. No shortcuts. Takes ~30 minutes.

---

## Day 0 — Same-day (within 2 hours of yes)

- [ ] Send **thank-you email** with: Stripe/ACH invoice for 50% deposit, contract (`sales/contract-template.md` with their info filled in), intake form (`sales/intake-form.md`).
- [ ] Create client folder: `cp -r clients/_template clients/<slug>` (slug = lowercase-dashed business name).
- [ ] Fill in `clients/<slug>/00-brief.md` with what you know from the discovery call.
- [ ] Add them to your Stripe customer list with their legal name + email.
- [ ] Add 3-day follow-up reminder in case the deposit doesn't hit.

## Day 1–3 — Waiting for signature + deposit + intake

- [ ] Don't start building. Not even "just the easy part." Wait.
- [ ] If it's been 3 days with no response, send one nudge: "Hey, just checking — need anything from me to get this rolling?"

## Deposit clears + contract signed + intake returned — kickoff day

- [ ] File signed contract in `clients/<slug>/01-scope-and-contract.md` (paste the full signed text or attach PDF).
- [ ] File intake answers in `clients/<slug>/00-brief.md`.
- [ ] Book kickoff call on calendar (30 min). Use the agenda from `ops/kickoff-checklist.md`.
- [ ] Block out the delivery window on your calendar (timeline per service).
- [ ] Create the working repo/folder for their build (separate from the Jaybird repo — never push client work here).
- [ ] Request credentials — email them `ops/credentials-policy.md` so they know what to share and how.

## Kickoff call day

Run through `ops/kickoff-checklist.md`.

## During the build

- [ ] Check in every 3 business days even if nothing's changed. Silence = client anxiety.
- [ ] Log significant decisions in `clients/<slug>/03-kickoff-notes.md`.
- [ ] Save every deliverable as you go to `clients/<slug>/04-deliverables/`.
- [ ] Don't batch 14 questions into one email — send them as they come, client will pick the ones they care about.

## Delivery day

Run `ops/handoff-checklist.md`.

---

## First-client checklist (ONCE, before first paying client)

Do these BEFORE your first client signs, not after:

- [ ] Stripe account live, can send invoices
- [ ] Business bank account separate from personal (Nevada LLC or sole prop with DBA)
- [ ] EIN from IRS
- [ ] Nevada State Business License (required for LLC/LLP/Corp)
- [ ] Clark County + Las Vegas business licenses if operating in those jurisdictions
- [ ] Google Workspace with jay@jaybirdautomations.com (looks more pro than gmail)
- [ ] Calendly or similar booking link → live on website
- [ ] Professional contract template reviewed by a Nevada small-business attorney
- [ ] General liability insurance quote (Hiscox, Next, Thimble — $30–$60/mo typical)
- [ ] Password manager (1Password family/business, Bitwarden) — non-negotiable
