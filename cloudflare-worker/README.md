# Jaybird Chat — Cloudflare Worker Setup

## Quick Start (5 minutes)

### 1. Create a Cloudflare Account
- Go to https://dash.cloudflare.com and sign up (free)

### 2. Create the Worker
- Go to **Workers & Pages** → **Create** → **Create Worker**
- Name it `jaybird-chat`
- Click **Deploy** (deploys the default hello world)
- Click **Edit Code** and paste the contents of `worker.js`
- Click **Deploy**

### 3. Add Environment Variables
Go to your worker → **Settings** → **Variables and Secrets**:

| Variable | Value |
|----------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (sk-ant-...) |
| `SUPABASE_URL` | Your Supabase project URL (optional, for lead storage) |
| `SUPABASE_KEY` | Your Supabase anon key (optional) |
| `ALLOWED_ORIGIN` | `https://jaybirdautomations.github.io` |

> Make `ANTHROPIC_API_KEY` and `SUPABASE_KEY` **encrypted** (click the lock icon).

### 4. Update the Chat Widget
In `chatbot/chat-widget.js`, replace:
```js
const WORKER_URL = 'https://jaybird-chat.YOUR-SUBDOMAIN.workers.dev';
```
with your actual worker URL (shown at the top of the worker page).

### 5. (Optional) Set Up Supabase for Lead Storage
- Go to https://supabase.com and create a free project
- Go to **SQL Editor** and run:

```sql
CREATE TABLE chat_leads (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  email TEXT,
  name TEXT,
  phone TEXT,
  service_interest TEXT,
  conversation_summary TEXT,
  source TEXT DEFAULT 'chatbot'
);

-- Allow the worker to insert rows
ALTER TABLE chat_leads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow insert from service role" ON chat_leads
  FOR INSERT WITH CHECK (true);
```

- Get your project URL and anon key from **Settings → API**

## Cost Estimate
- Cloudflare Worker: **Free** (100,000 requests/day)
- Claude Haiku API: **~$0.25 per 1M input tokens** (~$5-15/month at moderate traffic)
- Supabase: **Free** (500MB database, 50K monthly active users)

## Testing
After deployment, open your website and click the chat button. Try:
- "What services do you offer?"
- "How much does an AI commercial cost?"
- "I'm a restaurant owner in Las Vegas, can you help me?"
