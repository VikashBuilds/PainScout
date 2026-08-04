# 🚀 HostageFree

*Escape platform lock-in, keep your data, stop forced updates*

## The problem
Platforms like Adobe, Proton, and WhatsApp threaten account deactivation to force updates and deliberately block downgrades or exports, trapping paying customers in hostile ecosystems.

## The solution
HostageFree monitors your connected accounts for dark patterns (forced updates, downgrade blocks, export barriers), alerts you via WhatsApp before you're trapped, and automates one-click data export and migration to open alternatives.

## Features (v1)
- WhatsApp alerts for forced-update threats and downgrade blocks
- Automated data export from Google, Adobe, Proton, Apple, Microsoft
- Risk dashboard scoring each account's lock-in severity (0-100)
- One-tap migration guides to open-source alternatives (LibreOffice, Nextcloud, Signal, etc.)
- Pre-filled cancellation/downgrade forms with legal templates
- Platform policy change monitor (ToS, pricing, feature removals)
- Scheduled auto-backups before forced-update deadlines
- Community-sourced dark-pattern database with user reports
- Verified account closure with data-receipt confirmation
- Developer API to add custom platform connectors

## MVP scope
Build WhatsApp bot that OAuth-connects to Google, Adobe, and Proton; scans for forced-update notices and downgrade restrictions; sends real-time WhatsApp alerts; provides one-click export links and migration checklists. Core: WhatsApp webhook, 3 platform connectors, alert engine, simple React dashboard.

## Tech stack
Node.js/TypeScript, Express + Prisma ORM, WhatsApp Business API (Meta Cloud API), Puppeteer/Playwright for scraping non-API platforms, PostgreSQL (Supabase), Redis (Upstash) for queues, OpenAI GPT-4o for policy analysis, Railway hosting + Cron jobs

## Build estimate: 21 days

## Competitors & gaps
- **JustDeleteMe** — gap: Static deletion links only; no monitoring, no WhatsApp, no migration paths, no real-time alerts
- **AccountKiller** — gap: Manual guides only; no automation, no account health scoring, no cross-platform export
- **MyDataDoneRight** — gap: Enterprise B2B focus ($500+/mo); no consumer WhatsApp bot, no forced-update detection
- **Google Takeout / Adobe Export** — gap: Platform-specific, manual, one-time; no cross-platform dashboard, no downgrade assistance
- **SimpleLogin / AnonAddy** — gap: Email aliasing only; doesn't address storage, creative cloud, or OS-level lock-in

## Landing page copy
- **Headline:** Stop Letting Platforms Hold Your Data Hostage
- **Subheadline:** Get warned before forced updates trap you. One-tap export. Seamless migration. All from WhatsApp.
- Bullet: 🚨 Real-time WhatsApp alerts when apps threaten deactivation
- Bullet: 📦 One-click export from Adobe, Proton, Google, Apple, Microsoft
- Bullet: 🧭 Migration checklists to open-source alternatives (LibreOffice, Nextcloud, Signal)
- Bullet: 📉 Downgrade/cancel with pre-filled legal forms — no dark patterns
- Bullet: 📊 Lock-in risk score (0-100) for every connected account
- Bullet: ⏰ Auto-backup scheduler before forced-update deadlines
- **CTA:** Connect WhatsApp & Scan Free

## WhatsApp-first bot
- **Flow:** User clicks 'Connect WhatsApp' on landing page → OAuth to Google/Adobe/Proton → Bot runs initial risk scan → Sends risk report with scores → User replies with commands to export, migrate, or downgrade → Bot executes and confirms
- **Commands:** SCAN — re-run risk check on all linked accounts, EXPORT [platform] — generate download link for full data dump, MIGRATE [from] [to] — step-by-step guide (e.g., MIGRATE ADOBE LIBREOFFICE), ALERTS — toggle real-time notifications on/off, DOWNGRADE [platform] — pre-filled cancellation form + support chat template, ALTERNATIVES [platform] — ranked open-source/privacy-first replacements, SCORE — show current lock-in risk scores for all accounts
- **Pricing:** Freemium: 3 platforms free forever. Pro $9/mo or $79/yr: unlimited platforms, auto-export scheduler, priority alerts, API access, verified closure receipts.

## Pricing model: $9/mo SaaS, freemium (3 platforms), $79/yr pro
