# 🚀 ScamShield AI

*AI guardian that stops WhatsApp scams, spam, and catfishers before they reach you*

## The problem
WhatsApp users are flooded with scams, catfishing, and spam from unknown contacts, with no effective filtering, reporting, or privacy controls — leading to financial losses up to $500k.

## The solution
A WhatsApp-native AI bot that screens unknown senders, analyzes messages for scam patterns in real-time, and gives users granular privacy controls to block, report, and auto-filter threats without leaving the app.

## Features (v1)
- Real-time scam detection on forwarded messages using AI (LLM + heuristic rules)
- Unknown contact screening: auto-reply with verification challenge before delivering to user
- Group protection: bot monitors groups for suspicious links, impersonation, investment scams
- Privacy dashboard: control who can message, see profile, add to groups via simple commands
- One-tap reporting: forward to bot, it files report with WhatsApp and authorities
- Scam database: community-sourced known scam numbers, patterns, updated daily
- Link sandbox: auto-expand and analyze shortened URLs for phishing/malware
- Catfish detection: reverse image search on profile pics, consistency checks
- Custom rules: user-defined keywords, regex, sender patterns to auto-block
- Daily digest: summary of blocked attempts, threats caught, privacy score

## MVP scope
Build a WhatsApp bot (via Twilio/WhatsApp Business API) that users can forward messages to for instant AI scam analysis, with a simple dashboard to manage blocklists and view threat logs. Core: message forwarding endpoint, AI classification (OpenAI GPT-4o + custom rules), user management, basic privacy controls via chat commands.

## Tech stack
Node.js/TypeScript with Fastify, WhatsApp Business API via Twilio, OpenAI GPT-4o for classification, PostgreSQL (Supabase) for user data and logs, Redis + BullMQ for async job queue, Railway for hosting, Next.js for admin dashboard, Sentry for error monitoring

## Build estimate: 21 days

## Competitors & gaps
- **Truecaller** — gap: Focuses on calls/SMS, not WhatsApp; no AI scam analysis for WhatsApp messages
- **WhatsApp built-in reporting** — gap: Slow, no feedback, no proactive filtering, no privacy controls
- **Android spam blocker apps** — gap: Require notification access, don't work on iOS, no AI analysis
- **Meta Privacy Checkup** — gap: Educational only, no automation, no real-time protection
- **ScamAdviser** — gap: Website checker only, not integrated into WhatsApp

## Landing page copy
- **Headline:** Stop WhatsApp Scams Before They Cost You
- **Subheadline:** AI guardian that screens unknown contacts, detects catfishers, and auto-filters spam — all inside WhatsApp.
- Bullet: Forward any suspicious message → instant AI verdict: scam, spam, or safe
- Bullet: Auto-challenge unknown senders with verification questions before they reach you
- Bullet: Block investment scams, romance catfish, phishing links, and fake job offers in real-time
- Bullet: One-tap reporting to WhatsApp & authorities with evidence package
- Bullet: Privacy dashboard: control who sees your profile, adds you to groups, messages you
- **CTA:** Add ScamShield to WhatsApp Free

## WhatsApp-first bot
- **Flow:** User adds bot contact → sends 'START' → bot explains commands → user forwards suspicious messages → bot replies with analysis + action buttons → user manages privacy via chat commands.
- **Commands:** SCAN <forwarded message>, BLOCK <number>, ALLOW <number>, PRIVACY, REPORT <number>, SETTINGS, HELP
- **Pricing:** Freemium: 10 scans/day free. Pro $4.99/mo for unlimited scans, auto-screening, group protection, priority support.

## Pricing model: Freemium SaaS: $4.99/mo Pro, $39/yr, lifetime $99. Free tier: 10 AI scans/day, basic blocking.
