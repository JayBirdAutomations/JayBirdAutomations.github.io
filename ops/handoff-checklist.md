# Handoff Checklist

Run this EVERY time you deliver a project. Even retainer sub-deliverables. It's the difference between "Jay built us a site" and "Jay's my guy."

---

## Before handoff call — the day before

- [ ] Final QA pass:
    - [ ] Mobile (375px, 768px, 1440px)
    - [ ] Desktop (1280px, 1920px)
    - [ ] Lighthouse ≥ 85 desktop, ≥ 70 mobile
    - [ ] All forms submit + land where they should
    - [ ] All links work
    - [ ] No console errors
    - [ ] Favicon + Open Graph image present
    - [ ] 404 page works
    - [ ] GA4 tag fires (check real-time view)
- [ ] All credentials transferred to client accounts
- [ ] Remove any "jay's dev stuff" — staging branches, test data, debug flags

## Handoff call — 45 min

### 1. Walkthrough (15 min)
- Screen-share the live site/system
- Show each major feature working
- Record the call → save Loom to `clients/<slug>/04-deliverables/handoff-walkthrough.mp4`

### 2. How to maintain it (15 min)
- Show them exactly how to:
    - Edit copy / add a page / upload a photo
    - Check chatbot conversations
    - View analytics
    - Pause or edit the blog generator
    - Update DNS/domain if they switch providers
- Save short Loom for each ("How to edit your about page")

### 3. Support terms (5 min)
- 30-day bug-fix guarantee. Bugs = broken vs spec. New features = new quote.
- How to reach you (email + phone + expected response time)
- Retainer offer if applicable

### 4. The ask (5 min) — IMPORTANT
- **Testimonial ask:** "If you're happy with this, would you write a short testimonial I can put on my site? 2–3 sentences about the outcome, your name + photo."
- **Google review ask:** Send them the direct link to your GBP review form. Same day as handoff is when they're most likely to write it.
- **Case study ask:** "Can I document this project (with real numbers, or anonymized if you prefer) as a case study?"
- **Referral ask:** "If you know anyone else who could use this, I'll throw you 10% of their project as a thank-you." Send them a Calendly link to share.

### 5. Close (5 min)
- Send final invoice on the call while they're still warm.
- Book a 30-day post-launch check-in on calendar.

## After handoff — same day

- [ ] Send follow-up email with:
    - Loom links (walkthrough + maintenance)
    - All credentials (via password manager share link, NEVER email)
    - Final invoice
    - Testimonial/review/referral reminders
- [ ] Move client folder: `mv clients/<slug> clients/_delivered/<slug>` OR tag as delivered in a top-level `clients/_index.md`
- [ ] Archive the working repo/folder
- [ ] Add to portfolio (`jay-n8n-portfolio.html` or a new case-studies section)
- [ ] Log revenue in your bookkeeping

## 30 days later

- [ ] Check-in call or email: "How's it running? Any questions? Anything broken?"
- [ ] If retainer upsell wasn't closed at handoff, ask again now with 30 days of data as the hook: "You saw X leads this month — imagine what that looks like compounding."
