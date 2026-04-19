# Clients

One folder per paying client. No exceptions.

## Spinning up a new client

```bash
# From repo root:
cp -r clients/_template "clients/<slug>"
```

Where `<slug>` = the client's business name, lowercase, dashes. Examples: `rossi-law`, `desert-auto`, `momo-pizza-vegas`.

Then fill in (in order):
1. `00-brief.md` — what you know so far
2. `01-scope-and-contract.md` — paste signed scope / contract
3. `02-credentials.md` — pointers to your password manager (NOT actual values)
4. `03-kickoff-notes.md` — running log of decisions
5. `04-deliverables/` — every file you hand over
6. `05-invoices/` — copies of each invoice sent
7. `06-handoff.md` — the wrap-up

## Lifecycle

- **Active:** `clients/<slug>/`
- **Delivered:** `clients/_delivered/<slug>/` (move after handoff)
- **Inactive retainer (churned):** `clients/_archived/<slug>/` (move 30 days after last invoice)

Keep the folder forever. You'll need the history if they come back OR if they refer someone.

## What's in `_template/`

A blank skeleton. Copy, don't edit the template directly.
