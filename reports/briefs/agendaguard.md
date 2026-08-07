# 🚀 AgendaGuard

*Stop unprepared meetings before they hit your calendar*

## The problem
65% of meeting organizers skip agendas, forcing knowledge workers into 30+ hours/week of aimless calls that push real work to nights and weekends.

## The solution
AgendaGuard integrates with calendars to block meeting invites lacking agendas, auto-generates prep docs from past context, and scores meeting health so attendees can decline waste confidently.

## Features (v1)
- Calendar sync (Google/Outlook) with real-time invite scanning for agenda presence
- Auto-decline or flag meetings missing structured agendas with customizable rules
- AI agenda generator (GPT-4o) creating draft agendas from title, attendees, past notes
- Meeting health score (0-100) rating agenda quality, attendee count, duration, recurrence
- One-click prep doc compilation pulling relevant Slack threads, emails, docs, prior notes
- Attendee RSVP actions: 'Accept with prep', 'Decline — no agenda', 'Tentative — need clarity'
- Organizer nudges via Slack/email 24h and 2h before meeting to add agenda
- Weekly analytics dashboard: hours saved, meetings declined, prep compliance by team
- WhatsApp bot for daily summaries, quick RSVP, and on-the-go agenda generation
- Template library: proven agenda structures for standups, retros, 1:1s, decisions, planning

## MVP scope
Build Google Calendar sync + agenda detection + auto-decline/flag logic first. Add AI agenda generator with 3 templates (standup, 1:1, decision). Ship WhatsApp bot for 'check my day' summary and PREP/DECLINE commands. Onboard 10 beta users from HN/Reddit for feedback loop.

## Tech stack
Next.js 14 (App Router), Supabase (Postgres + Auth + Realtime), Google Calendar API + Microsoft Graph API, OpenAI GPT-4o, Vercel (hosting + edge functions), Upstash Redis (rate limiting, caching), Resend (transactional email), Twilio WhatsApp Business API

## Build estimate: 21 days

## Competitors & gaps
- **Fellow.app** — gap: Focuses on collaborative note-taking during meetings; doesn't prevent bad meetings from being scheduled
- **Calendly** — gap: Scheduling only — no agenda enforcement, quality scoring, or prep automation
- **Microsoft Teams/Google Meet built-ins** — gap: Agenda field exists but is optional, unenforced, and invisible to attendees pre-RSVP
- **Reclaim.ai** — gap: Time-blocking for focus time; doesn't address meeting prep quality or organizer accountability
- **Doodle** — gap: Scheduling polls only; zero prep enforcement or meeting health visibility

## Landing page copy
- **Headline:** Reclaim 15+ Hours/Week by Blocking Unprepared Meetings
- **Subheadline:** AgendaGuard auto-rejects calendar invites without agendas, generates prep docs instantly, and scores every meeting so you only attend what matters.
- Bullet: Auto-decline or flag meetings missing agendas — no more empty calendar slots
- Bullet: AI generates structured agendas from title, attendees, and past context in seconds
- Bullet: Meeting health scores (0-100) let you decline waste with data, not guilt
- Bullet: One-click prep docs compile Slack, email, and docs before every call
- Bullet: Weekly analytics show hours saved and prep compliance across your org
- **CTA:** Join the Beta — Free for 3 Months

## WhatsApp-first bot
- **Flow:** User connects calendar via OAuth link. Bot sends daily 8 AM summary: '3 meetings today, 1 missing agenda ⚠️'. User replies 'PREP 2' to get AI-generated agenda for meeting #2, 'DECLINE 1' to auto-decline meeting #1, 'SCORE' for health scores. Organizers get 2h nudge: 'Add agenda to "Q3 Planning" or it gets flagged.'
- **Commands:** PREP [num], DECLINE [num], SCORE, TODAY, WEEK, TEMPLATES, HELP
- **Pricing:** Free tier: 10 meeting checks/mo. Pro: $12/mo unlimited checks, AI agenda gen, WhatsApp bot, analytics. Team: $10/user/mo org-wide enforcement, admin dashboard, SSO.

## Pricing model: $12/mo per user Pro, $10/user/mo Team (min 5 seats), freemium 10 checks/mo
