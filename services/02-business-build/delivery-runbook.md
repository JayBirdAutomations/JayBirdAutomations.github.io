# 02 — Business Build

**Price:** $3,999 flat · **Timeline:** 10–14 days · **Deposit:** $2,000 (50%)

## What's included

Everything in Quick Launch, PLUS:
- AI Chatbot (trained on client's services + FAQs)
- AI Blog Engine (auto-publishes weekly posts via n8n)
- Lead capture integration (chatbot → email/CRM)
- Extended SEO (blog sitemap, article schema, AIO/llms.txt)
- 2 rounds of revisions

## Source files

- Website: `index.html` base
- Chatbot: `chatbot/chat-widget.js`, `chatbot/chat-widget.css`, `cloudflare-worker/worker.js`
- Blog: `blog/template.html`, `blog/posts.json`, `blog/index.html`, `workflows/blog-generator.json`

## Delivery steps

1. Steps 1–11 from `services/01-quick-launch-website/delivery-runbook.md`.
2. Install chatbot — follow `services/04-ai-chatbot/delivery-runbook.md`.
3. Install blog engine — follow `services/05-ai-blog-engine/delivery-runbook.md`.
4. Write chatbot knowledge base from intake form answers.
5. Seed 3 launch blog posts (don't wait for n8n cron).
6. Handoff — includes chatbot admin tour + how the blog auto-runs.

## Deliverables checklist

- [ ] All Quick Launch deliverables
- [ ] Chatbot live and answering correctly (test 10 questions)
- [ ] Blog with 3 posts live
- [ ] Blog generator n8n workflow deployed in client's n8n instance OR yours (decide up front)
- [ ] Weekly cron tested (manual trigger once)
- [ ] Client trained on: editing chatbot knowledge base, pausing blog, checking GA4

## Upsells

- Growth Retainer ($4,999/mo) — ongoing content, SEO, feature additions
- AI Commercial ($1,499) — launch video for their new site
