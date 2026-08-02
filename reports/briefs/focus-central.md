# 🚀 Focus Central

*Stop switching. Start doing.*

## The problem
Busy professionals waste hours each day jumping between tasks, notes, calendars, and chat apps, losing focus and control over their workflow.

## The solution
Focus Central unifies all your work streams into one keyboard-driven command palette, letting you capture, schedule, and act without context switching. Its AI parser turns free text into tasks, events, and notes, while a WhatsApp bot lets you manage everything from your pocket.

## Features (v1)
- Global command palette (Ctrl/Cmd+K) for instant access to tasks, notes, calendar, and chat
- Natural language input: "Lunch with Alex tomorrow 12pm" becomes an event with reminder
- Unified inbox with tabs for Tasks, Notes, Calendar, and Messages
- Google Calendar and Todoist integrations (read/write) to sync existing commitments
- AI auto-categorization of triaged chat messages into action items or reference notes
- Focus timer that auto-blocks deep work slots in your calendar
- Weekly review email: accomplishments, unfinished tasks, and schedule insights
- WhatsApp bot for quick capture and retrieval on the go
- Keyboard-first navigation with vi-style shortcuts for power users
- Local cache and offline mode for uninterrupted access

## MVP scope
Build a single-page web app with a command palette UI that stores tasks, notes, and events in Supabase. Integrate Google Calendar read-only and WhatsApp Business Cloud API for text-based task/note capture. Use OpenAI API to parse natural language input into structured items. No chat dashboard or offline mode in the first iteration.

## Tech stack
Next.js 14 (App Router), TypeScript, Tailwind CSS, Supabase (Postgres, Auth, Realtime), Google Calendar API, OpenAI API (gpt-4o-mini), WhatsApp Business Cloud API, Vercel (hosting)

## Build estimate: 12 days

## Competitors & gaps
- **Notion** — gap: All-in-one workspace but requires heavy setup and still lacks a unified command palette to bridge external tools and chat.
- **Taskade** — gap: Collaborative task management but no WhatsApp capture and weak cross-app integration for calendar and email.
- **Zapier** — gap: Automation across apps but overly complex for individuals and doesn't provide a single focused UI for daily work.
- **RescueTime** — gap: Tracks time after the fact but doesn't help capture and act on tasks in real-time.

## Landing page copy
- **Headline:** Your whole workspace. One keystroke away.
- **Subheadline:** Stop losing focus between apps — control tasks, notes, calendar, and chat from a single command palette.
- Bullet: [
- Bullet: '
- Bullet: S
- Bullet: u
- Bullet: m
- Bullet: m
- Bullet: o
- Bullet: n
- Bullet:  
- Bullet: a
- Bullet: n
- Bullet: y
- Bullet:  
- Bullet: a
- Bullet: c
- Bullet: t
- Bullet: i
- Bullet: o
- Bullet: n
- Bullet:  
- Bullet: w
- Bullet: i
- Bullet: t
- Bullet: h
- Bullet:  
- Bullet: C
- Bullet: t
- Bullet: r
- Bullet: l
- Bullet: /
- Bullet: C
- Bullet: m
- Bullet: d
- Bullet: +
- Bullet: K
- Bullet: '
- Bullet: ,
- Bullet:  
- Bullet: '
- Bullet: A
- Bullet: I
- Bullet:  
- Bullet: p
- Bullet: a
- Bullet: r
- Bullet: s
- Bullet: e
- Bullet: s
- Bullet:  
- Bullet: f
- Bullet: r
- Bullet: e
- Bullet: e
- Bullet:  
- Bullet: t
- Bullet: e
- Bullet: x
- Bullet: t
- Bullet:  
- Bullet: i
- Bullet: n
- Bullet: t
- Bullet: o
- Bullet:  
- Bullet: t
- Bullet: a
- Bullet: s
- Bullet: k
- Bullet: s
- Bullet: ,
- Bullet:  
- Bullet: e
- Bullet: v
- Bullet: e
- Bullet: n
- Bullet: t
- Bullet: s
- Bullet: ,
- Bullet:  
- Bullet: a
- Bullet: n
- Bullet: d
- Bullet:  
- Bullet: n
- Bullet: o
- Bullet: t
- Bullet: e
- Bullet: s
- Bullet: '
- Bullet: ,
- Bullet:  
- Bullet: '
- Bullet: W
- Bullet: o
- Bullet: r
- Bullet: k
- Bullet: s
- Bullet:  
- Bullet: w
- Bullet: i
- Bullet: t
- Bullet: h
- Bullet:  
- Bullet: t
- Bullet: o
- Bullet: o
- Bullet: l
- Bullet: s
- Bullet:  
- Bullet: y
- Bullet: o
- Bullet: u
- Bullet:  
- Bullet: a
- Bullet: l
- Bullet: r
- Bullet: e
- Bullet: a
- Bullet: d
- Bullet: y
- Bullet:  
- Bullet: u
- Bullet: s
- Bullet: e
- Bullet: '
- Bullet: ,
- Bullet:  
- Bullet: '
- Bullet: C
- Bullet: a
- Bullet: p
- Bullet: t
- Bullet: u
- Bullet: r
- Bullet: e
- Bullet:  
- Bullet: a
- Bullet: n
- Bullet: y
- Bullet: t
- Bullet: h
- Bullet: i
- Bullet: n
- Bullet: g
- Bullet:  
- Bullet: v
- Bullet: i
- Bullet: a
- Bullet:  
- Bullet: W
- Bullet: h
- Bullet: a
- Bullet: t
- Bullet: s
- Bullet: A
- Bullet: p
- Bullet: p
- Bullet: ,
- Bullet:  
- Bullet: g
- Bullet: e
- Bullet: t
- Bullet:  
- Bullet: r
- Bullet: e
- Bullet: m
- Bullet: i
- Bullet: n
- Bullet: d
- Bullet: e
- Bullet: r
- Bullet: s
- Bullet:  
- Bullet: i
- Bullet: n
- Bullet:  
- Bullet: f
- Bullet: l
- Bullet: o
- Bullet: w
- Bullet: '
- Bullet: ]
- **CTA:** Get early access

## WhatsApp-first bot
- **Flow:** Users message the bot in natural language. The bot replies with a parsed action (task/note/event) and confirms creation. Users can reply /list to see today's items, or /focus to start a session.
- **Commands:** [, ', /, t, a, s, k, ', ,,  , ', /, n, o, t, e, ', ,,  , ', /, e, v, e, n, t, ', ,,  , ', /, l, i, s, t, ', ,,  , ', /, t, o, d, a, y, ', ,,  , ', /, f, o, c, u, s, ', ]
- **Pricing:** Free tier: 100 messages/month. Paid: $9/month for unlimited messages and smart reminders.

## Pricing model: $15/mo per user, 14-day free trial
