# Jaybird Blog Generator — N8N Workflow

Autonomous blog publisher. Every Monday at 9 AM PT (or on manual trigger), it:

1. Picks a random topic from a hardcoded queue
2. Asks Claude Haiku 4.5 to write a full SEO-optimized blog post
3. Builds a styled HTML file matching Jaybird branding
4. Commits the post to `blog/posts/{slug}.html` on GitHub
5. Updates `blog/posts.json` so the blog index shows it
6. Appends the post URL to `sitemap.xml`

GitHub Pages auto-deploys — post goes live within ~30 seconds of commit.

---

## Setup (one time, ~5 minutes)

### 1. Import the workflow

In N8N: **Workflows → Import from File** → select `blog-generator.json`.

### 2. Set environment variables

The workflow reads two env vars via `{{ $env.VAR }}`. Set them in N8N:

**N8N Cloud / self-hosted:** Settings → Environment Variables
**Docker:** add to `docker-compose.yml` under `environment:`

| Variable | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com/ → API Keys → Create Key |
| `GITHUB_TOKEN` | https://github.com/settings/tokens → Generate new token (classic) → scopes: `repo` (full control of private repositories) |

> **Note:** `ANTHROPIC_API_KEY` is currently empty in the project `.env`. You'll need to create one at console.anthropic.com before the workflow can run.

### 3. Verify the GitHub repo path

The workflow hits `JayBirdAutomations/JayBirdAutomations.github.io`. If your repo name is different, search-and-replace that string in these 6 node URLs:

- GitHub: Create Post File
- GitHub: Get posts.json
- GitHub: Put posts.json
- GitHub: Get sitemap.xml
- GitHub: Put sitemap.xml

### 4. Test run

1. Open the workflow → click **Execute Workflow** (manual trigger)
2. Watch each node turn green
3. Check your repo for a new commit: `Blog: <title>`
4. Visit https://jaybirdautomations.com/blog/ — the new post should appear on the index
5. Click it — full styled article with schema, CTA, GA4 tracking

### 5. Activate the schedule

Toggle **Active** (top right) to enable the weekly Monday 9 AM cron.

---

## How it works

```
Manual Trigger ─┐
                ├─▶ Pick Topic ─▶ Claude API ─▶ Build HTML ─▶
Weekly Cron  ───┘

  ─▶ GitHub: Create Post File
  ─▶ GitHub: Get posts.json ─▶ Update posts.json ─▶ GitHub: Put posts.json
  ─▶ GitHub: Get sitemap.xml ─▶ Update sitemap.xml ─▶ GitHub: Put sitemap.xml
```

### Pick Topic node

Random pick from a hardcoded list of 15 evergreen topics. To add or remove topics, edit the `topics` array inside the node's Code editor. For a more sophisticated queue (mark used, track history), swap this node for a Google Sheets read/write.

### Claude API node

- Model: `claude-haiku-4-5-20251001` (~$0.03 per post)
- max_tokens: 4000
- System prompt enforces: no hype, Las Vegas angle, H2/H3 structure, lists, CTA at end
- Response must be valid JSON matching the schema: `title`, `slug`, `meta_description`, `excerpt`, `body_html`, `tags`

### Build HTML node

Inlines the full post HTML (template + content) as a single string — no external template fetch needed. Base64-encodes it for the GitHub API.

The template matches the main site:
- Same nav header and brand gradient
- Article Schema.org JSON-LD
- BreadcrumbList schema
- OpenGraph + Twitter meta
- GA4 tracking (G-2PLT037V1Q)
- Book-a-Call CTA at the bottom

### GitHub commits

Three commits per run:
1. `Blog: <title>` — creates the post HTML file
2. `Blog manifest: <title>` — updates posts.json
3. `Sitemap: add <slug>` — updates sitemap.xml

---

## Editing the Claude prompt

All prompt engineering lives in the **Claude API** node's `jsonBody` field. Look for the `"content": "..."` string. Tune it as you learn what works:

- Want longer posts? Change "800-1200 words" to your target.
- Want a different voice? Edit the system prompt at the top.
- Want industry-specific posts? Pass `industry` alongside `topic` from the Pick Topic node.

---

## Troubleshooting

**"JSON parse error" in Build HTML**
Claude occasionally wraps JSON in markdown fences. The node strips them, but if Claude hallucinates additional text, increase `max_tokens` or tighten the system prompt ("Return ONLY JSON, no other text").

**"404 Not Found" on GitHub nodes**
Either the repo path is wrong (see step 3) or the `GITHUB_TOKEN` doesn't have `repo` scope.

**Post appears in repo but not on site**
GitHub Pages takes 30–90 seconds to deploy. Hard-refresh (Ctrl+Shift+R).

**Want to rollback a bad post**
`git revert <commit-sha>` on the main branch. The workflow never deletes — it only adds.

---

## Cost per post

| Item | Cost |
|---|---|
| Claude Haiku 4.5 (~2k input + 2k output tokens) | ~$0.03 |
| GitHub API | Free |
| GitHub Pages hosting | Free |
| **Total** | **~$0.03** |

52 posts/year = ~$1.56 in API costs. You'll spend more on coffee.
