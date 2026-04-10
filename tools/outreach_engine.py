"""
Jaybird Automations — Email Outreach Engine
Sends personalized cold emails using Brevo (ex-Sendinblue) API.

SETUP:
1. Sign up at https://www.brevo.com (free: 300 emails/day)
2. Get your API key: Settings → SMTP & API → API Keys
3. Set environment variable: BREVO_API_KEY=your-key
4. Set environment variable: ANTHROPIC_API_KEY=your-key (for personalization)
5. Buy a separate outreach domain (e.g., jaybirdai.com) — $12/year
6. Set up SPF, DKIM, DMARC on that domain in Brevo

IMPORTANT: Warm up your domain for 2 weeks before sending outreach!
Start with 10 emails/day, increase by 5/day each week.

USAGE:
  python outreach_engine.py send --batch 10              # Send to 10 new leads
  python outreach_engine.py send --lead-id 42            # Send to specific lead
  python outreach_engine.py followup                     # Send due follow-ups
  python outreach_engine.py preview --lead-id 42         # Preview email without sending
  python outreach_engine.py test --email your@email.com  # Send test to yourself
  python outreach_engine.py stats                        # Show outreach stats
"""

import os
import sys
import json
import sqlite3
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Load .env file automatically (keys stay off the command line and out of chat)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / '.env')
except ImportError:
    pass

# ─── CONFIG ───────────────────────────────────────────────────────────
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Your sender info — UPDATE THESE
SENDER_NAME = "Jay | Jaybird Automations"
SENDER_EMAIL = "jay@jaybirdautomations.com"
PHYSICAL_ADDRESS = "Las Vegas, NV 89101"  # Use PO Box or registered agent address
PHONE = ""

BREVO_API_URL = "https://api.brevo.com/v3"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "jaybird_leads.db")

# Follow-up schedule (days after initial email)
FOLLOWUP_SCHEDULE = [3, 7, 14]


# ─── EMAIL TEMPLATES ──────────────────────────────────────────────────

TEMPLATES = {
    "initial": {
        "law firm": {
            "subject": "Question about {business_name}",
            "body": """Hi,

I was looking up law firms in Las Vegas and came across {business_name}. {personalization_line}

Most firms I talk to are dealing with the same problem — too many hours spent on things that aren't billable. Intake calls, follow-up emails, scheduling, chasing paperwork. It adds up fast.

I work with a few local businesses here in Las Vegas helping them cut that overhead so they can focus on the work that actually brings in revenue. Usually takes a couple weeks to set up and pays for itself quickly.

Not sure if it's a fit for your firm, but would it be worth a 15-minute call to find out?

Jay
Jaybird Automations | Las Vegas, NV
jay@jaybirdautomations.com
jaybirdautomations.com

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
        },

        "restaurant": {
            "subject": "Question for {business_name}",
            "body": """Hi,

I found {business_name} while looking at restaurants in Las Vegas. {personalization_line}

One thing I see a lot with local restaurants — they're putting out great food but struggling to get consistent new customers through the door. Most of the marketing they try is either too expensive or just doesn't convert.

I help local businesses here in Vegas fix that. The approach is different for every business, but the goal is always the same — more revenue without just throwing money at ads.

Would it make sense to jump on a quick 15-minute call? No pitch, just want to understand what's working and what isn't for {business_name} right now.

Jay
Jaybird Automations | Las Vegas, NV
jay@jaybirdautomations.com
jaybirdautomations.com

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
        },

        "dental office": {
            "subject": "Quick question for {business_name}",
            "body": """Hi,

I came across {business_name} while researching dental practices in Las Vegas. {personalization_line}

A lot of practices I talk to have the same bottleneck — the front desk is overwhelmed, appointment no-shows are eating into revenue, and follow-up with patients falls through the cracks. It's hard to grow when the admin side is holding you back.

I help local businesses streamline those exact problems. It's not a one-size-fits-all thing — I look at what's actually costing the most time and money and fix that first.

Would a 15-minute call be worth it to see if I could help {business_name}?

Jay
Jaybird Automations | Las Vegas, NV
jay@jaybirdautomations.com
jaybirdautomations.com

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
        },

        "contractor": {
            "subject": "Question for {business_name}",
            "body": """Hi,

I found {business_name} while looking at contractors in Las Vegas. {personalization_line}

Most contractors I speak with are great at the work but losing jobs because of slow follow-up on estimates or leads that go cold over the weekend. By the time Monday comes around, the customer already called someone else.

I help local businesses fix that kind of leak — so more of the leads you're already getting actually turn into paying jobs.

Worth a quick 15-minute call to see if there's something there for {business_name}?

Jay
Jaybird Automations | Las Vegas, NV
jay@jaybirdautomations.com
jaybirdautomations.com

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
        },

        "default": {
            "subject": "Quick question for {business_name}",
            "body": """Hi,

I came across {business_name} while researching businesses in Las Vegas. {personalization_line}

I work with local businesses here in Vegas helping them find and fix the biggest bottleneck holding back their growth — whether that's losing leads after hours, spending too much time on admin, or struggling to get consistent new customers.

Every business is different, so I don't lead with a solution until I understand the problem. That's why I'd rather start with a quick conversation than pitch you something you don't need.

Would 15 minutes be worth it to see if I could help {business_name}?

Jay
Jaybird Automations | Las Vegas, NV
jay@jaybirdautomations.com
jaybirdautomations.com

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
        }
    },

    "followup_1": {
        "subject": "Re: {original_subject}",
        "body": """Hi,

Just following up in case my last email got buried.

I did a quick look at {business_name}'s online presence and found a few things worth sharing — no cost, no obligation. Just thought it might be useful.

Happy to send it over if you're curious.

Jay
Jaybird Automations | Las Vegas, NV"""
    },

    "followup_2": {
        "subject": "Re: {original_subject}",
        "body": """Hi,

I'll keep this short — I recently helped a Las Vegas business fix a growth problem they'd been stuck on for over a year. Took about three weeks to implement. They're still seeing the results.

If the timing ever makes sense for {business_name}, I'm easy to reach.

Jay
Jaybird Automations | Las Vegas, NV

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
    },

    "followup_3": {
        "subject": "Re: {original_subject}",
        "body": """Hi,

I won't keep following up after this — I know your inbox is busy.

If things change and {business_name} ever wants a fresh set of eyes on a growth problem, feel free to reach out anytime.

Good luck with everything.

Jay
Jaybird Automations | Las Vegas, NV

Feel free to reply directly to this email — I read and respond to every message personally.

To opt out: {unsubscribe_link} | {physical_address}"""
    }
}


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def generate_personalization(lead):
    """Use Claude to generate a personalized opening line based on lead data."""
    if not ANTHROPIC_API_KEY:
        # Fallback without AI
        if not lead.get("website"):
            return "I noticed you don't have a website listed — that's a huge opportunity to reach more customers online."
        return "I thought there might be some ways AI could help streamline your operations."

    prompt = f"""Write a single, short, conversational sentence that a salesperson would use as a personalized observation about this business. It should naturally follow "I was looking at [business] online and..."

Business: {lead.get('business_name', '')}
Industry: {lead.get('industry', '')}
Website: {lead.get('website', 'none')}
Google Rating: {lead.get('google_rating', 'unknown')}
Reviews: {lead.get('review_count', 'unknown')}
Has Chatbot: {'yes' if lead.get('has_chatbot') else 'no'}
Website Score: {lead.get('website_score', 'not analyzed')}

Rules:
- One sentence only, under 30 words
- Sound natural and observational, not salesy
- If no website: mention they're missing online presence
- If low reviews: mention opportunity for more visibility
- If no chatbot: mention after-hours lead capture opportunity
- Never be negative or insulting about their business"""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        if resp.ok:
            return resp.json()["content"][0]["text"].strip().strip('"')
    except Exception as e:
        print(f"  Warning: Claude API error, using fallback: {e}")

    # Fallback
    if not lead.get("website"):
        return "I noticed you don't have a website listed — that's a huge opportunity."
    return "I thought there might be some ways AI could help streamline your operations."


def build_email(lead, template_type="initial", followup_num=0):
    """Build a personalized email for a lead."""
    industry = lead.get("industry", "default")

    if template_type == "initial":
        templates = TEMPLATES["initial"]
        template = templates.get(industry, templates["default"])
        personalization = generate_personalization(dict(lead))
    else:
        template = TEMPLATES.get(f"followup_{followup_num}", TEMPLATES["followup_3"])
        personalization = ""

    # Build unsubscribe link (Brevo handles this, but we add a placeholder)
    unsubscribe_link = "click here to unsubscribe: {{unsubscribe}}"  # Brevo replaces {{unsubscribe}} with the actual URL

    subject = template["subject"].format(
        business_name=lead["business_name"],
        original_subject=f"AI tools for {lead['business_name']}"
    )

    body = template["body"].format(
        business_name=lead["business_name"],
        personalization_line=personalization,
        phone=PHONE,
        unsubscribe_link=unsubscribe_link,
        physical_address=PHYSICAL_ADDRESS,
        original_subject=f"AI tools for {lead['business_name']}"
    )

    return subject, body


def send_email(to_email, to_name, subject, body):
    """Send an email via Brevo API."""
    if not BREVO_API_KEY:
        print("ERROR: Set BREVO_API_KEY environment variable")
        print("Sign up free at https://www.brevo.com")
        return False

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "textContent": body,
    }

    resp = requests.post(
        f"{BREVO_API_URL}/smtp/email",
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=15
    )

    if resp.ok:
        return True
    else:
        print(f"  Brevo error: {resp.status_code} — {resp.text}")
        return False


def is_on_dnc_list(email):
    """Check if email is on do-not-contact list."""
    conn = get_db()
    row = conn.execute("SELECT id FROM do_not_contact WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row is not None


def log_outreach(lead_id, email_type, template_used, subject):
    """Log an outreach attempt."""
    conn = get_db()
    conn.execute(
        "INSERT INTO outreach_log (lead_id, email_type, template_used, subject) VALUES (?, ?, ?, ?)",
        (lead_id, email_type, template_used, subject)
    )
    conn.execute(
        "UPDATE leads SET status = 'contacted', last_contacted = datetime('now') WHERE id = ?",
        (lead_id,)
    )
    conn.commit()
    conn.close()


def send_batch(batch_size=10):
    """Send initial outreach to a batch of new leads."""
    conn = get_db()
    leads = conn.execute(
        "SELECT * FROM leads WHERE status = 'new' AND email IS NOT NULL AND email != '' ORDER BY lead_score DESC LIMIT ?",
        (batch_size,)
    ).fetchall()
    conn.close()

    if not leads:
        print("No new leads with email addresses to contact.")
        print("TIP: Run the lead prospector first, then import leads into the database.")
        return

    sent = 0
    skipped = 0

    for lead in leads:
        email = lead["email"]
        if not email or is_on_dnc_list(email):
            skipped += 1
            continue

        print(f"  Sending to: {lead['business_name']} ({email})")
        subject, body = build_email(dict(lead), "initial")

        if send_email(email, lead["business_name"], subject, body):
            log_outreach(lead["id"], "initial", lead.get("industry", "default"), subject)
            sent += 1
        else:
            skipped += 1

    print(f"\nSent: {sent} | Skipped: {skipped}")


def send_followups():
    """Send follow-up emails to leads that are due."""
    conn = get_db()

    for followup_num, days_after in enumerate(FOLLOWUP_SCHEDULE, 1):
        cutoff_date = (datetime.now() - timedelta(days=days_after)).isoformat()

        # Find leads that were contacted but haven't received this follow-up
        leads = conn.execute("""
            SELECT l.* FROM leads l
            WHERE l.status = 'contacted'
              AND l.last_contacted <= ?
              AND l.email IS NOT NULL AND l.email != ''
              AND NOT EXISTS (
                SELECT 1 FROM outreach_log o
                WHERE o.lead_id = l.id AND o.email_type = ?
              )
            ORDER BY l.lead_score DESC
            LIMIT 20
        """, (cutoff_date, f"followup_{followup_num}")).fetchall()

        if not leads:
            continue

        print(f"\nFollow-up #{followup_num} (day {days_after}): {len(leads)} leads due")

        for lead in leads:
            if is_on_dnc_list(lead["email"]):
                continue

            subject, body = build_email(dict(lead), "followup", followup_num)
            print(f"  Sending follow-up #{followup_num} to: {lead['business_name']}")

            if send_email(lead["email"], lead["business_name"], subject, body):
                log_outreach(lead["id"], f"followup_{followup_num}", f"followup_{followup_num}", subject)

    conn.close()


def preview_email(lead_id):
    """Preview an email without sending."""
    conn = get_db()
    lead = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    conn.close()

    if not lead:
        print(f"Lead #{lead_id} not found")
        return

    subject, body = build_email(dict(lead), "initial")

    print(f"\n{'='*60}")
    print(f"  TO: {lead['business_name']} <{lead.get('email', 'NO EMAIL')}>")
    print(f"  FROM: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"  SUBJECT: {subject}")
    print(f"{'='*60}")
    print(body)
    print(f"{'='*60}\n")


def send_test(test_email):
    """Send a test email to yourself using the real default template."""
    # Use a fake lead so the test shows the actual current template
    fake_lead = {
        "business_name": "Sample Business Co.",
        "industry": "default",
        "website": "",
        "google_rating": 3.8,
        "review_count": 12,
        "has_chatbot": False,
        "website_score": 4,
    }
    subject, sample_body = build_email(fake_lead, "initial")
    subject = f"[TEST] {subject}"
    body = f"""This is a TEST email from the Jaybird Outreach Engine.
Sender: {SENDER_NAME} <{SENDER_EMAIL}>
Sent at: {datetime.now().isoformat()}

--- ACTUAL EMAIL YOUR LEADS WILL RECEIVE ---

{sample_body}"""

    print(f"Sending test email to: {test_email}")
    if send_email(test_email, "Test Recipient", subject, body):
        print("Test email sent successfully! Check your inbox.")
    else:
        print("Failed to send test email. Check your Brevo API key and sender domain.")


def show_stats():
    """Show outreach statistics."""
    conn = get_db()
    total_sent = conn.execute("SELECT COUNT(*) FROM outreach_log").fetchone()[0]
    initial_sent = conn.execute("SELECT COUNT(*) FROM outreach_log WHERE email_type = 'initial'").fetchone()[0]
    followups_sent = conn.execute("SELECT COUNT(*) FROM outreach_log WHERE email_type LIKE 'followup%'").fetchone()[0]
    replied = conn.execute("SELECT COUNT(*) FROM leads WHERE status = 'replied'").fetchone()[0]
    meetings = conn.execute("SELECT COUNT(*) FROM leads WHERE status = 'meeting'").fetchone()[0]
    clients = conn.execute("SELECT COUNT(*) FROM leads WHERE status = 'client'").fetchone()[0]
    dnc = conn.execute("SELECT COUNT(*) FROM do_not_contact").fetchone()[0]
    conn.close()

    reply_rate = (replied / initial_sent * 100) if initial_sent > 0 else 0
    meeting_rate = (meetings / initial_sent * 100) if initial_sent > 0 else 0

    print(f"\n{'='*50}")
    print(f"  OUTREACH STATS")
    print(f"{'='*50}")
    print(f"  Total Emails Sent:    {total_sent}")
    print(f"    Initial:            {initial_sent}")
    print(f"    Follow-ups:         {followups_sent}")
    print(f"  Replies:              {replied} ({reply_rate:.1f}%)")
    print(f"  Meetings Booked:      {meetings} ({meeting_rate:.1f}%)")
    print(f"  Clients Won:          {clients}")
    print(f"  Do-Not-Contact List:  {dnc}")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="Jaybird Email Outreach Engine")
    subparsers = parser.add_subparsers(dest="command")

    s = subparsers.add_parser("send", help="Send initial outreach emails")
    s.add_argument("--batch", type=int, default=10, help="Number of leads to email")
    s.add_argument("--lead-id", type=int, help="Send to a specific lead ID")

    subparsers.add_parser("followup", help="Send due follow-up emails")

    p = subparsers.add_parser("preview", help="Preview email for a lead")
    p.add_argument("--lead-id", type=int, required=True, help="Lead ID to preview")

    t = subparsers.add_parser("test", help="Send test email to yourself")
    t.add_argument("--email", type=str, required=True, help="Your email address")

    subparsers.add_parser("stats", help="Show outreach statistics")

    args = parser.parse_args()

    if args.command == "send":
        if args.lead_id:
            conn = get_db()
            lead = conn.execute("SELECT * FROM leads WHERE id = ?", (args.lead_id,)).fetchone()
            conn.close()
            if lead and lead["email"]:
                subject, body = build_email(dict(lead), "initial")
                if send_email(lead["email"], lead["business_name"], subject, body):
                    log_outreach(lead["id"], "initial", lead.get("industry", "default"), subject)
                    print(f"Sent to {lead['business_name']}")
            else:
                print("Lead not found or has no email")
        else:
            send_batch(args.batch)
    elif args.command == "followup":
        send_followups()
    elif args.command == "preview":
        preview_email(args.lead_id)
    elif args.command == "test":
        send_test(args.email)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
