# Credentials Policy

**Rule #1: Never put live credentials in git. Ever.**

---

## Where credentials live

| Credential type | Where it goes |
|---|---|
| Your own (Jaybird) API keys, DB passwords | Password manager (1Password / Bitwarden) |
| Per-client API keys, DB passwords | Password manager, separate vault per client |
| Quick-reference placeholder | `clients/<slug>/02-credentials.md` — **gitignored**, placeholders only, real values in PM |
| `.env` files in code | Local only, never committed, `.env.example` checked in with fake values |

## The client vault pattern

In your password manager, create one vault per active client:
- Name: `JA · <Client Legal Name>`
- Shared with: only you (or team if you hire)
- Archived after 1 year of inactivity, never deleted

Each vault holds:
- Domain registrar login
- Hosting login
- GA4 + Search Console
- CMS/backend admins
- Third-party tool logins (Stripe, HubSpot, their n8n, etc.)
- API keys Jaybird provisions on their behalf

## How to RECEIVE credentials from clients

**Accept:**
- Shared password manager entry (best — 1Password family share, Bitwarden share link with expiry, LastPass share)
- Encrypted ZIP via Wetransfer with password sent separately
- Live on-screen during Zoom (you type while they read — they never send it)

**Refuse:**
- Email with password in the body
- Slack DM with password
- Text message with password
- Anything in a Google Doc they didn't restrict

If client insists on an insecure method → politely insist once, then move on but NEVER store it somewhere unsecured on your side.

## How to SEND credentials to clients

**Accept:**
- Password manager share link (preferred — 1Password, Bitwarden both support time-limited public links)
- Bitwarden Send (expiring one-time link)
- On a live screen-share where they save into their own PM

**Refuse:**
- Email
- Slack / Discord / Teams DM
- Text

## The `02-credentials.md` file

This file lives in every client folder. It's a **reference** to what credentials exist — NOT the actual values.

Example contents:
```markdown
# [Client Name] — Credentials Reference

All real values are in 1Password vault: "JA · [Client Name]"

| System | Username | Vault entry name |
|---|---|---|
| Cloudflare | jay@jaybirdautomations.com | JA · [Client] · Cloudflare |
| GA4 (property ID: 123456) | jay@jaybirdautomations.com | JA · [Client] · Google |
| n8n cloud | jay@jaybirdautomations.com | JA · [Client] · n8n |
| Client's domain registrar | [client email] | JA · [Client] · Domain |

## Access notes
- Client owns the GA4 property; Jay has "editor" access
- Client owns Cloudflare; Jay invited as admin
- n8n is Jay-hosted (per contract clause 4.2)
```

This file IS committed to git. Values in PM. Perfectly safe.

## When a client project ends

Within 30 days of final handoff:
- Remove Jay's login from client-owned accounts (GA4, Cloudflare, hosting, etc.)
- Revoke API keys Jaybird provisioned that client was using
- Archive the PM vault (don't delete — keep for 1 year in case of support request)
- Keep `clients/<slug>/02-credentials.md` as a historical reference (with a note: "ACCESS REVOKED [DATE]")

## If a credential leaks

- Rotate it IMMEDIATELY (all affected systems).
- Tell the client within 24 hours. Even if it was their fault. Even if nothing happened.
- Write it up briefly in `clients/<slug>/incidents.md` with date + what was rotated.

## .gitignore

Double-check that `.gitignore` in the repo root includes:
```
# Client credentials — never commit
clients/**/02-credentials.md
clients/**/credentials/
clients/**/*.env
clients/**/secrets.*
```

If `02-credentials.md` IS meant to be committed (the reference-only version), remove the pattern. But the file should then contain ZERO real values — only pointers to the PM vault.

**When in doubt: assume git is public. Because one accidental push makes it public forever.**
