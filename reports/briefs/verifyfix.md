# 🚀 VerifyFix

*Unlock WhatsApp when iOS verification loops block your account*

## The problem
iPhone users get stuck in a false 'update required' loop during WhatsApp phone verification — the app rejects the current App Store build, won't send SMS/call codes, and locks them out of their accounts with no in-app escape hatch.

## The solution
VerifyFix is an AI-powered troubleshooting bot that runs on WhatsApp itself (via a backup number or web) and guides users through proven, version-specific workarounds — cache clears, network resets, TestFlight builds, Apple ID region tricks, and escalation templates — until verification succeeds. It learns from each success to update its playbook in real time.

## Features (v1)
- Interactive diagnostic flow that detects iOS version, WhatsApp build, carrier, and error variant
- Step-by-step video + text guides for 12 known iOS verification failure patterns
- One-tap 'Open WhatsApp TestFlight' deep link when public build is broken
- Auto-generated Apple Support & WhatsApp Support tickets with device logs attached
- Fallback verification via WhatsApp Business API sandbox (receive code in our chat)
- Push alert when WhatsApp acknowledges the bug or pushes a hotfix
- Community-sourced workaround voting so the best fix bubbles up
- Privacy-first: no phone number stored, all logic runs client-side via Shortcuts
- iOS Shortcut export for one-tap 'Nuclear Reset' (delete app, keychain, network settings)
- Admin dashboard showing real-time failure heatmap by region/carrier/iOS version

## MVP scope
Ship a WhatsApp Business API bot + iOS Shortcut that runs a 5-question diagnostic, serves the top 3 fixes for the detected error pattern, and logs success/failure to a Supabase table. No dashboard, no community, no push alerts — just the bot, the shortcut, and a landing page.

## Tech stack
Node.js + Fastify on Fly.io, WhatsApp Cloud API (Meta Business), Supabase (Postgres + Realtime + Auth), OpenAI GPT-4o-mini for dynamic fix generation, iOS Shortcuts (JSON export) for client-side automation, Tailwind CSS + Astro for landing page, Resend for transactional email (support tickets), Sentry for error tracking

## Build estimate: 14 days

## Competitors & gaps
- **WhatsApp FAQ / In-app Help** — gap: Generic articles; no version-specific, interactive troubleshooting; can't reach you when you're locked out
- **Apple Support App** — gap: Routes to generic 'reinstall app' advice; no WhatsApp-specific logic; 24-48h response
- **Reddit / Twitter / DownDetector** — gap: Crowdsourced but unstructured; no guided fix; high noise; no privacy
- **Third-party 'WhatsApp Fixer' Android apps** — gap: Android-only; often malware; no iOS support; no official API access
- **MobileTrans / Dr.Fone (desktop tools)** — gap: $40-60 one-time; requires PC/Mac; overkill for verification-only issue; no WhatsApp bot

## Landing page copy
- **Headline:** Stuck on 'Update WhatsApp' when you're already updated?
- **Subheadline:** VerifyFix gets you back in — no laptop, no Apple Store visit, no waiting on hold.
- Bullet: Works from a friend's WhatsApp or the web — no account access needed
- Bullet: Fixes 12+ iOS verification error patterns in under 3 minutes
- Bullet: Exports a one-tap iOS Shortcut for the 'nuclear reset'
- Bullet: Auto-files a pre-filled WhatsApp Support ticket with your logs
- Bullet: Free while in beta; $4.99/mo after for unlimited recoveries
- **CTA:** Start Fixing on WhatsApp →

## WhatsApp-first bot
- **Flow:** User messages 'VERIFY' to +1-555-VERIFY-1 → Bot replies with 5 diagnostic buttons (iOS version, WhatsApp version, carrier, error screenshot, tried fixes) → User taps → Bot serves top 3 fixes with video GIFs + 'Run Shortcut' button → User reports result → Bot logs success/failure, offers escalation ticket if failed
- **Commands:** VERIFY — start diagnostic, SHORTCUT — get iOS Shortcut file, TICKET — generate support ticket PDF, STATUS — check known outage map, HELP — show all commands
- **Pricing:** Free tier: 3 recoveries/month. Pro: $4.99/mo unlimited + priority shortcut updates + email ticket backup. Team: $19/mo for 5 seats + admin dashboard.

## Pricing model: Freemium SaaS: $4.99/mo per user (Pro), $19/mo per 5-seat team. No per-lead; usage capped only by recovery count on free tier.
