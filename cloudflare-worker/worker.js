/**
 * Jaybird Automations — Cloudflare Worker
 * Proxies chat requests to Claude API and stores leads in Supabase.
 *
 * DEPLOYMENT:
 * 1. Go to https://dash.cloudflare.com → Workers & Pages → Create Worker
 * 2. Paste this code
 * 3. Add these environment variables (Settings → Variables):
 *    - ANTHROPIC_API_KEY: your-anthropic-api-key
 *    - SUPABASE_URL: your-supabase-project-url
 *    - SUPABASE_KEY: your-supabase-secret-key
 *    - ALLOWED_ORIGIN: https://jaybirdautomations.com
 * 4. Deploy and note the worker URL (e.g., https://jaybird-chat.xxx.workers.dev)
 * 5. Update WORKER_URL in chatbot/chat-widget.js with that URL
 */

const SYSTEM_PROMPT = `You are Jaybird AI, the assistant for Jaybird Automations — an AI agency in Las Vegas run by Jay.

STYLE (strict):
- Keep replies to 2–3 short sentences max. Never write paragraphs.
- Sound like a friendly human texting, not a brochure. Contractions, warmth, zero corporate fluff.
- One idea per reply. If the visitor needs more, they'll ask.
- No bullet lists unless the visitor explicitly asks for a list.
- Mirror the visitor's energy — short question gets a short answer.

WHAT WE DO (keep it simple when asked):
- Website upgrades with AI (chat, lead capture, smart forms)
- Lead generation & business automation (find customers, automate follow-up)
- Custom AI software development (apps, dashboards, tools built from scratch)
- AI agents & digital workers (autonomous assistants that handle tasks 24/7)
- n8n workflow creation (YouTube pipelines, CRM triggers, social media automation)
- AI commercials (broadcast-quality video, days not weeks)

PRICING (only share if asked):
- Quick Launch $1,499/project — N8N workflows, AI commercials
- Business Build $3,999/project — website enhancement, lead gen, automation & CRM
- Growth Retainer $4,999/month — 3 projects/month, any service mix, dedicated strategist
- Enterprise custom — AI software development, AI agents
Say the price and what it covers, then offer a call. Don't list all tiers at once.

LEAD CAPTURE:
When someone shows real interest, casually ask for their name + email so Jay can follow up. One ask, not a form. Never pushy.

BOOKING: Point interested visitors to the contact form on the page or jay@jaybirdautomations.com.

If you don't know something, say so and offer to connect them with Jay.`;

export default {
  async fetch(request, env) {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN || '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Only accept POST to /chat
    const url = new URL(request.url);
    if (url.pathname !== '/chat' || request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Not found' }), {
        status: 404,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    try {
      const body = await request.json();
      const { messages, leadCaptured } = body;

      if (!messages || !Array.isArray(messages)) {
        return new Response(JSON.stringify({ error: 'Invalid request' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Rate limiting: simple IP-based check (basic protection)
      // For production, use Cloudflare's rate limiting rules

      // Call Claude API
      const claudeResponse = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 180,
          system: SYSTEM_PROMPT,
          messages: messages.slice(-10) // Keep last 10 messages for context
        })
      });

      if (!claudeResponse.ok) {
        const errText = await claudeResponse.text();
        console.error('Claude API error:', errText);
        throw new Error('Claude API error');
      }

      const claudeData = await claudeResponse.json();
      const reply = claudeData.content[0].text;

      // Check if the conversation contains lead info (email pattern)
      let newLeadCaptured = leadCaptured || false;
      const fullConversation = messages.map(m => m.content).join(' ') + ' ' + reply;
      const emailMatch = fullConversation.match(/[\w.-]+@[\w.-]+\.\w{2,}/);

      if (emailMatch && !leadCaptured) {
        newLeadCaptured = true;
        // Store lead in Supabase
        if (env.SUPABASE_URL && env.SUPABASE_KEY) {
          try {
            await fetch(`${env.SUPABASE_URL}/rest/v1/chat_leads`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'apikey': env.SUPABASE_KEY,
                'Authorization': `Bearer ${env.SUPABASE_KEY}`,
                'Prefer': 'return=minimal'
              },
              body: JSON.stringify({
                email: emailMatch[0],
                conversation_summary: fullConversation.slice(0, 2000),
                source: 'chatbot',
                created_at: new Date().toISOString()
              })
            });
          } catch (e) {
            console.error('Supabase error:', e);
          }
        }
      }

      return new Response(JSON.stringify({
        reply: reply,
        leadCaptured: newLeadCaptured
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (err) {
      console.error('Worker error:', err);
      return new Response(JSON.stringify({
        error: 'Something went wrong',
        reply: "I'm having trouble right now. Please email Jay directly at jay@jaybirdautomations.com!"
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
