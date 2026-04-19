# 05 — AI Blog Engine

**Price:** $1,500 setup + $500/mo (includes 4 posts/mo) · **Timeline:** 5 days

## Source files

- `blog/index.html` — blog listing page (Aurora Circuit themed)
- `blog/template.html` — post template with full SEO (OG, Twitter, Article + Breadcrumb schema)
- `blog/posts.json` — manifest that the listing reads
- `blog/posts/*.html` — one file per post
- `workflows/blog-generator.json` — n8n workflow that generates + commits posts

## How it works

Weekly cron in n8n → LLM generates topic + post → writes HTML from template → appends to posts.json → git commits → GitHub Pages auto-deploys.

## Delivery steps

1. **Intake:**
   - Business category (auto repair? law firm? restaurant?)
   - Target keywords (10–15, for SEO focus)
   - Target reader (owner? customer? both?)
   - Brand voice
   - Topics to AVOID (competitor names, sensitive issues)
   - Posting frequency (weekly default)

2. **Scaffold blog on their site:**
   - Create `/blog/` directory
   - Copy + rebrand `blog/index.html` to client palette
   - Copy `blog/template.html`
   - Create empty `blog/posts.json` with `{ "posts": [] }`

3. **Configure n8n workflow:**
   - Import `workflows/blog-generator.json` into client's n8n (or yours).
   - Set environment: `CLIENT_DOMAIN`, `GITHUB_REPO`, `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, `BUSINESS_NICHE`, `TARGET_KEYWORDS`.
   - Update the topic-generation prompt with their niche + voice.
   - Update sitemap-update node to point at their sitemap.xml.

4. **Seed 3 launch posts manually** — don't leave the blog empty. Pick 3 high-value topics from their keyword list and generate them now.

5. **Enable weekly cron** — Monday mornings work well (fresh content start of week).

6. **Sitemap + SEO:**
   - Add `/blog/` to client's main sitemap.xml
   - Add blog schema to each post (already in template.html)
   - Verify first post indexes in Search Console within 7 days

7. **Handoff:**
   - Show client how to pause the workflow
   - Show how to edit/delete a post if one publishes wrong
   - Set expectation: quality check is ON YOU for the first month, then spot-check monthly

## Deliverables checklist

- [ ] Blog listing live at /blog/
- [ ] 3 seeded posts published
- [ ] n8n workflow active, next run scheduled
- [ ] Sitemap updated
- [ ] Test run fired manually, commit went through
- [ ] Client trained on pause/edit

## Known watchpoints

- Dedupe check: the generator currently does NOT check for duplicate titles before writing. Before scaling, add a title-uniqueness check to the workflow. (See Jaybird's own blog 2026-04-19 cleanup.)
- Posts.json grows — if > 100 posts, paginate the blog index.
- Rate limits: Anthropic API — not a problem at weekly cadence.

## Pricing tiers within this service

- **$1,500 setup + $500/mo** — 4 posts/mo, client's brand, client's n8n
- **$1,500 setup + $99/mo** — 1 post/mo, Jay hosts n8n
- **Add-on for retainer clients** — included at 4 posts/mo as part of Growth Retainer
