# 🚀 SoloStack

*Lightweight MongoDB dashboards & auth that just work for indie devs*

## The problem
Solo founders waste days configuring enterprise tools like Metabase and Auth0 for simple MongoDB visualization and user auth, while lightweight alternatives lack trust and reliability.

## The solution
SoloStack provides a zero-config MongoDB dashboard and authentication layer that deploys in minutes. It combines visual query building, auto-generated admin panels, and battle-tested auth (email/password, OAuth, magic links) — all without the bloat of enterprise platforms.

## Features (v1)
- Auto-generated MongoDB admin UI with CRUD, filters, and relation browsing
- Visual query builder → charts/dashboards (no MQL/SQL needed)
- Auth: email/password, magic links, Google/GitHub OAuth, JWT tokens
- React/React Native SDK + REST API for custom frontends
- Role-based access control (admin, editor, viewer) out of the box
- One-click deploy to Railway/Render/Fly.io with managed MongoDB
- Audit logs & GDPR export/delete endpoints
- Embeddable dashboards for customer-facing analytics
- CLI for local dev & schema migrations
- Self-hosted or cloud with solo-dev friendly pricing

## MVP scope
Ship a self-hosted Docker image that connects to any MongoDB URI, auto-generates an admin panel with CRUD + charts, and issues JWTs via email/password + Google OAuth. Skip multi-tenancy, embeddable dashboards, and CLI in v1.

## Tech stack
Next.js 14 (App Router, API routes, server actions), Prisma ORM (MongoDB connector, type-safe queries), NextAuth.js v5 (auth providers, JWT sessions, adapters), Recharts (visualization, responsive charts), Tailwind CSS + shadcn/ui (styling, accessible components), Docker + Docker Compose (packaging, local dev), Railway / Fly.io (recommended hosting, one-click deploy), Zod (validation, schema inference)

## Build estimate: 21 days

## Competitors & gaps
- **Metabase** — gap: Java-based, heavy resource usage, overkill for simple MongoDB; no built-in auth
- **Auth0** — gap: Complex setup, pricing spikes at scale, docs assume enterprise architecture
- **Firebase** — gap: Vendor lock-in, Firestore ≠ MongoDB, trust issues from Google sunset history
- **AdminBro** — gap: Requires custom code per resource, not zero-config, auth is DIY
- **PocketBase** — gap: SQLite-only, not MongoDB; auth mature but data layer wrong for this pain

## Landing page copy
- **Headline:** Stop Wrestling Metabase. Start Shipping.
- **Subheadline:** SoloStack gives you a production-ready MongoDB admin panel + auth in 5 minutes. Zero config. Self-hosted. Built for indie devs.
- Bullet: Auto-admin UI from your MongoDB collections
- Bullet: Visual dashboards — no query language needed
- Bullet: Auth with email, magic links, OAuth in one SDK
- Bullet: Deploy to Railway/Fly.io with one click
- Bullet: Self-hosted — your data, your server, your rules
- **CTA:** Deploy Free on Railway

## WhatsApp-first bot
- **Flow:** Dev connects MongoDB URI → bot provisions SoloStack instance → sends dashboard URL + auth credentials → dev manages users/collections via chat commands
- **Commands:** /connect <mongo_uri>, /deploy, /users, /collections, /dashboard, /logs
- **Pricing:** Free self-hosted; $19/mo managed cloud (includes hosting, backups, SSL)

## Pricing model: Free self-hosted (MIT); $19/mo managed cloud with auto-backups, SSL, custom domain; $49/mo team (SSO, audit logs, priority support)
