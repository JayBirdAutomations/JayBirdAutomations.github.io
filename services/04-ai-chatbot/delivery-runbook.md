# 04 — AI Chatbot

**Price:** $500–$1,500 (depends on knowledge base depth + integrations) · **Timeline:** 3–5 days

## Source files

All three are required:
- `chatbot/chat-widget.js` — the embeddable widget
- `chatbot/chat-widget.css` — widget styles
- `cloudflare-worker/worker.js` — the backend that talks to Claude API

## How it works

1. Widget embeds on client's site with 2 lines of HTML.
2. User types question → widget hits Cloudflare Worker endpoint.
3. Worker prepends system prompt (knowledge base) → calls Claude API → streams response back.
4. Widget displays response + optional lead capture form.

## Delivery steps

1. **Intake** — collect knowledge base inputs:
   - Services/products list (with prices if they share them)
   - Top 20 FAQs and answers
   - Brand voice (friendly? formal? Las Vegas casual?)
   - What counts as a "qualified lead" (for capture trigger)
   - Escalation: when chatbot can't answer, what happens? (email, phone, "book a call")

2. **Deploy worker** — fork `cloudflare-worker/` into client's Cloudflare account (or yours, depending on agreement). Set env vars:
   - `ANTHROPIC_API_KEY`
   - `SYSTEM_PROMPT` (the knowledge base)
   - `LEAD_WEBHOOK_URL` (where to POST captured leads)

3. **Customize widget** — in `chatbot/chat-widget.css`, swap colors to match client brand. Update greeting + avatar in `chatbot/chat-widget.js`.

4. **Write knowledge base** — structure:
   ```
   You are [Client Name]'s AI assistant.

   About us: [2–3 sentences]
   Services: [bulleted list with prices]
   Hours: [hours]
   Location: [address + service area]

   FAQs:
   Q: [question]
   A: [answer]

   When someone asks about pricing for a specific service, give the starting price and offer to connect them with [Client] for a quote.

   When someone asks to book/schedule, respond with: "Happy to help — here's our booking link: [URL]" OR capture name+email+phone and say Jay will reach out.

   Never make up services, prices, or policies not in this document. If you don't know, say: "Great question — let me have [Client] follow up on that. What's the best email to reach you at?"
   ```

5. **Test 20 questions** — real questions from the client's common customer. Edit knowledge base until 18/20 answer correctly.

6. **Embed** — add to client site:
   ```html
   <link rel="stylesheet" href="/chatbot/chat-widget.css">
   <script src="/chatbot/chat-widget.js" data-endpoint="https://[worker].workers.dev"></script>
   ```

7. **Lead capture test** — trigger a capture flow. Verify email/webhook fires.

8. **Handoff** — train client on: how to edit knowledge base (re-deploy worker), how to check conversation logs, how to pause if needed.

## Deliverables checklist

- [ ] Worker deployed, endpoint live
- [ ] Widget styled to brand
- [ ] 20-question test passed
- [ ] Lead capture tested end-to-end
- [ ] Client has Cloudflare access (or agreed to "Jay hosts it")
- [ ] Knowledge base saved to `clients/<slug>/04-deliverables/knowledge-base.md`
- [ ] Monthly maintenance offered ($99/mo — KB updates + log review)

## Pricing tiers within this service

- **$500** — Up to 15 FAQs, no integrations, Jay hosts worker
- **$1,000** — Up to 40 FAQs, 1 integration (email/Slack/Zapier), Jay hosts
- **$1,500** — Custom KB, 3 integrations, client's own Cloudflare account
