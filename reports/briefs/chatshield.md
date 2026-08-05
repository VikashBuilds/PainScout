# 🚀 ChatShield

*Bulletproof WhatsApp reliability for revenue-critical conversations.*

## The problem
Small businesses lose revenue when WhatsApp freezes, accounts get restricted without warning, OTPs fail, and years of chat history vanish — with zero human support to fix it.

## The solution
ChatShield adds a reliability layer on top of WhatsApp Business API: continuous encrypted backups, real-time health monitoring, OTP fallback via email/voice, one-click restore, and automated risk scoring — so you never lose a customer conversation.

## Features (v1)
- Automated daily encrypted message backups to S3/R2 with point-in-time recovery
- Real-time account health monitoring (freeze detection, restriction alerts via webhooks)
- OTP delivery fallback: receive verification codes via email, voice call, or authenticator app
- One-click chat restore to new device or after reinstall with full media support
- Restriction risk scoring based on messaging patterns, template usage, and velocity
- Automated compliance checks for message frequency, opt-in status, and template approvals
- Revenue-at-risk dashboard showing potential loss per unhealthy account
- Webhook alerts to Slack, Email, or Telegram for critical events (ban, OTP failure, backup failure)

## MVP scope
Build the backup engine (daily encrypted message sync to S3), health monitor (webhook-based status checks), OTP fallback (Twilio voice/email), and a single-page dashboard showing last backup, account status, and restore button. Defer AI appeal generator and team roles.

## Tech stack
Node.js (NestJS), PostgreSQL (Supabase), Redis + BullMQ, AWS S3 / Cloudflare R2, WhatsApp Business API (Meta), Twilio (Voice/Email OTP), Vercel (Hosting), TailwindCSS + React (Dashboard)

## Build estimate: 21 days

## Competitors & gaps
- **Twilio Conversations** — gap: No native WhatsApp backup/restore or account health monitoring
- **MessageBird** — gap: Lacks automated OTP fallback and restriction risk scoring
- **Wati.io** — gap: Focuses on marketing automation, not reliability/backup
- **Respond.io** — gap: No one-click chat restore or revenue-at-risk metrics
- **Generic SaaS backup tools** — gap: Ignore WhatsApp entirely; no API integration for message-level recovery

## Landing page copy
- **Headline:** Stop Losing Customers to WhatsApp Glitches
- **Subheadline:** The reliability layer Meta forgot to build. Backups, monitoring, OTP fallback, and instant restore — all in one dashboard.
- Bullet: 🔒 Encrypted daily backups — recover any chat in seconds
- Bullet: 📊 Real-time health scores — know before you're banned
- Bullet: 📞 OTP via voice/email — never locked out again
- Bullet: 💰 Revenue-at-risk view — see exactly what's on the line
- **CTA:** Start 14-Day Free Trial

## WhatsApp-first bot
- **Flow:** User adds ChatShield as a contact → sends 'START' → bot guides through Business Account linking via OAuth → configures backup schedule & alert channels → daily status updates sent via WhatsApp + dashboard access.
- **Commands:** START — link account & configure, STATUS — current health, last backup, risk score, BACKUP NOW — trigger immediate backup, RESTORE <date> — initiate point-in-time restore, ALERTS ON/OFF — toggle WhatsApp notifications, OTP TEST — send test OTP via voice/email
- **Pricing:** Included in $49/mo plan; bot access free for all paid tiers

## Pricing model: $49/mo per WhatsApp Business Account, 14-day free trial, includes 10GB backup storage + 100 OTP fallback credits/mo
