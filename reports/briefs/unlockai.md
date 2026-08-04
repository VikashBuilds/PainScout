# 🚀 UnlockAI

*AI-powered account recovery concierge that escalates lockouts to human resolution*

## The problem
Users get locked out of critical accounts (email, cloud, crypto, hosting) with automated KYC flags and zero human escalation paths, leaving them stranded for days.

## The solution
UnlockAI automates evidence collection, drafts platform-specific appeals, routes cases to verified escalation contacts, and provides a WhatsApp concierge that tracks every ticket until access is restored.

## Features (v1)
- Multi-platform lockout diagnosis wizard (Google, Microsoft, AWS, DigitalOcean, Coinbase, GitHub, Meta)
- Automated evidence package builder (screenshots, logs, identity docs, timestamped activity)
- Platform-specific appeal letter generator tuned to each provider's policies and terminology
- Verified escalation contact database (executive emails, trust & safety teams, regulatory channels)
- WhatsApp bot for real-time case tracking, document upload, and one-tap escalation triggers
- SLA countdown timer with auto-escalation at 24h/48h/72h and regulatory complaint filing
- Success-rate analytics per platform & lockout type with community-sourced win patterns
- One-click GDPR/CCPA/CFPB complaint generator with pre-filled evidence packets
- Team vault for shared account recovery (agencies, startups) with role-based access
- Post-recovery hardening checklist (2FA rotation, recovery codes, backup emails, passkeys)

## MVP scope
Build diagnosis wizard for top 5 platforms (Google, Microsoft, AWS, DigitalOcean, Coinbase), appeal generator with 3 templates per platform, WhatsApp bot for case intake + status updates, and a curated escalation contact sheet. Ship as $29/mo SaaS with 3 free appeals/month.

## Tech stack
Next.js 14 (App Router, React Server Components), OpenAI GPT-4o (appeal generation, evidence parsing), Supabase (Postgres, Auth, Realtime, Edge Functions), Twilio WhatsApp Business API (conversational bot), Vercel (hosting, cron jobs for SLA timers), Resend (transactional email for appeals), Stripe (billing, subscription management), Playwright (scraping/updating escalation contacts)

## Build estimate: 21 days

## Competitors & gaps
- **DoNotPay** — gap: Generic legal bot; no platform-specific escalation contacts or WhatsApp concierge
- **AccountRecovery.com** — gap: Manual service at $199+/case; no self-serve automation or SLA tracking
- **Google Account Recovery** — gap: Only works for Google; automated loops with zero human escalation path
- **Chargeback Gurus** — gap: Focused on payment disputes, not account lockouts or identity verification
- **Reddit/Forum DIY** — gap: Unreliable, outdated contacts; no tracking, SLA, or regulatory leverage

## Landing page copy
- **Headline:** Locked out of your digital life? Get human help in hours, not weeks.
- **Subheadline:** UnlockAI automates appeals, finds real escalation paths, and tracks your case on WhatsApp until access is restored.
- Bullet: Platform-specific appeals for Google, AWS, Coinbase, Microsoft, DigitalOcean
- Bullet: Verified executive & trust-and-safety contacts — not public support forms
- Bullet: WhatsApp concierge: upload docs, get updates, trigger escalations by replying 'ESCALATE'
- Bullet: SLA countdown + auto-regulatory filing (GDPR/CCPA) when providers ghost you
- Bullet: Post-recovery hardening so it never happens again
- **CTA:** Start Free Appeal →

## WhatsApp-first bot
- **Flow:** User sends 'LOCKED' → Bot asks platform & lockout type → User uploads screenshot/notice → Bot generates appeal + contacts → User approves → Bot emails appeal + tracks SLA → Auto-escalates at 24h/48h/72h → Notifies on WhatsApp at each step → User replies 'DONE' when restored.
- **Commands:** LOCKED, STATUS, ESCALATE, UPLOAD, DONE, TEMPLATES, CONTACTS
- **Pricing:** $29/mo includes 3 appeals/mo, WhatsApp concierge, escalation contacts. Extra appeals $9 each. Freemium: 1 free appeal forever.

## Pricing model: $29/mo SaaS, freemium (1 free appeal), per-appeal overage $9
