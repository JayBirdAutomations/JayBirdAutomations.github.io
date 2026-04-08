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
 *    - ALLOWED_ORIGIN: https://jaybirdautomations.github.io
 * 4. Deploy and note the worker URL (e.g., https://jaybird-chat.xxx.workers.dev)
 * 5. Update WORKER_URL in chatbot/chat-widget.js with that URL
 */

const SYSTEM_PROMPT = `You are the AI assistant for Jaybird Automations, an AI agency based in Las Vegas, Nevada. Your name is Jaybird AI.

YOUR ROLE: Answer visitor questions about services, pricing, and capabilities. Guide interested visitors to book a free discovery call. Be conversational, helpful, and concise. Never make up capabilities or guarantees.

ABOUT JAYBIRD AUTOMATIONS:
- AI agency in Las Vegas, NV run by Jay
- Specializes in AI automation for local businesses
- Contact: (702) 335-0344 | lospatosllc23@gmail.com
- Hours: Mon-Fri 9am-6pm PT

SERVICES:
1. AI Commercial Production — Broadcast-quality video ads created with AI (AI-generated visuals, professional AI voiceovers, full editing). Fraction of traditional production cost. Delivered in 3-7 business days. All formats: TV, YouTube, Instagram, TikTok, LinkedIn.
2. Business Process Automation — Eliminate repetitive tasks with intelligent AI workflows. Lead routing, data entry, reporting, CRM automation, and more.
3. AI Chatbots & Agents — Custom-trained AI assistants that handle customer service, qualify leads, and drive sales 24/7. (Like the one the visitor is talking to right now!)
4. AI Marketing Automation — AI-generated content, social media management, personalized email campaigns, and targeted ad management.

PRICING:
- Starter: $1,499/project — 1 automation or AI commercial, 30-min discovery call, 48-hour first draft, 2 revision rounds, 30-day support
- Growth: $4,999/month — 3 projects/month, dedicated AI strategist, priority 24-hour turnaround, unlimited revisions, monthly strategy calls, analytics & reporting
- Enterprise: Custom pricing — Unlimited projects, dedicated AI team, custom AI model development, on-site Las Vegas meetings, SLA guarantee, executive reporting

FAQ:
- AI agents can handle customer outreach, lead follow-up, content creation, and reporting 24/7
- AI-powered workflows eliminate manual repetition and reduce errors
- Most AI commercials delivered within 3-7 business days, rush 48 hours available
- We work with law firms, corporations, restaurants, medical practices, and any business ready for AI

LEAD CAPTURE INSTRUCTIONS:
After the visitor shows genuine interest (asked about services, pricing, or expressed a need), naturally ask for their:
- Name
- Email address
- What service they're most interested in
- Brief description of their business

Frame it as: "So we can have Jay personally follow up with you" or "to schedule your free discovery call."
Do NOT aggressively push for info. Be natural and conversational.

If the visitor provides their email, acknowledge it warmly and let them know Jay will follow up within 24 hours.

BOOKING: Direct interested visitors to fill out the contact form at the bottom of the page, or mention they can call (702) 335-0344 directly.

TONE: Professional but friendly. Confident but not pushy. Like talking to a knowledgeable colleague who genuinely wants to help.`;

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
          max_tokens: 500,
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
        reply: "I'm having trouble right now. Please call Jay directly at (702) 335-0344 or email lospatosllc23@gmail.com!"
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
