# 🚀 TriageAI

*Unify scanners, kill false positives, ship secure code faster*

## The problem
Security tools overwhelm developers with noisy false positives, opaque pricing hidden behind demos, and CISO-centric UX—forcing engineers to waste hours triaging alerts instead of shipping code.

## The solution
TriageAI unifies SAST, SCA, and secrets scanning into a single developer-first dashboard that auto-suppresses false positives using ML trained on 10M+ triage decisions, shows transparent per-seat pricing, and integrates natively into GitHub/GitLab PR workflows—so engineers fix real vulnerabilities in minutes, not hours.

## Features (v1)
- Unified dashboard aggregating Semgrep (SAST), OSV-Scanner (SCA), and TruffleHog (secrets) with deduplicated findings
- ML-powered false positive suppression learning from team accept/reject actions across 10M+ historical decisions
- One-click GitHub/GitLab PR annotations with AI-generated fix snippets and CWE context
- Transparent per-developer pricing at $15/dev/month — no sales calls, no contracts, cancel anytime
- Local CLI for pre-commit scanning (offline, zero code leaves machine) with SARIF output
- Slack/Teams alerts only for critical/exploitable findings with one-tap suppress or fix
- Custom rule packs for framework-specific patterns (React, Django, Go, Node, Python)
- Team-level noise baselines, trend tracking, and SOC2-ready SARIF/JSON exports
- Self-hosted Docker option for air-gapped environments (v1.1)
- GitHub App installation with fine-grained repo permissions and webhook-based scan triggers

## MVP scope
Build core aggregation engine connecting Semgrep, OSV-Scanner, and TruffleHog via CLI workers. Ship React dashboard with deduplicated findings view, false positive feedback loop (accept/reject trains per-team model), and GitHub PR comment integration. Package as GitHub App with Stripe per-seat billing. Defer self-hosted, custom rules, and Slack alerts to v1.1.

## Tech stack
Next.js 14 (App Router, TypeScript), PostgreSQL via Supabase (findings, teams, billing, ML feedback), Redis via Upstash + BullMQ (scan job queue, rate limiting), GitHub App + GitLab OAuth (auth, webhooks, PR comments), Semgrep, OSV-Scanner, TruffleHog as containerized scanner workers, OpenAI GPT-4o (fix snippet generation, CVE enrichment), Railway (hosting, managed Postgres/Redis, auto-deploy), Stripe Billing (per-seat subscriptions, portal, webhooks), TailwindCSS + shadcn/ui (dashboard components)

## Build estimate: 45 days

## Competitors & gaps
- **Snyk** — gap: Enterprise pricing, CISO dashboards, noisy defaults, no transparent per-seat cost
- **GitHub Advanced Security** — gap: Locked to GH ecosystem, expensive per-committer, limited SCA/secrets customization
- **Semgrep Cloud Platform** — gap: Great engine but no multi-scanner aggregation, pricing opaque after free tier
- **SonarCloud** — gap: Legacy UX, heavy false positives, built for compliance not developer velocity
- **Trivy** — gap: Excellent open-source scanner but no unified dashboard, triage workflow, or team features

## Landing page copy
- **Headline:** Stop drowning in security noise. Start shipping secure code.
- **Subheadline:** One dashboard. Three scanner engines. Zero false positives. Transparent pricing built for developers, not CISOs.
- Bullet: Unifies SAST, SCA, and secrets scanning in one view
- Bullet: ML suppresses 80%+ of false positives from day one
- Bullet: GitHub/GitLab PR comments with one-click fixes
- Bullet: $15/dev/month — no demos, no contracts, cancel anytime
- Bullet: Local CLI scans pre-commit — your code never leaves your machine
- Bullet: SOC2-ready exports for when compliance asks
- **CTA:** Start free 14-day trial — no credit card

## WhatsApp-first bot
- **Flow:** Dev forwards repo URL or pastes finding ID → Bot returns enriched context (CVE details, exploitability, fix snippet) → Dev replies 'suppress' or 'fix' → Bot updates dashboard and posts PR comment
- **Commands:** /scan <repo>, /findings <repo>, /suppress <finding-id>, /fix <finding-id>, /pricing, /help
- **Pricing:** Free for 1 repo, $15/dev/mo for unlimited — billed via Stripe link in chat

## Pricing model: $15/developer/month SaaS, 14-day free trial, no credit card required, cancel anytime. Unlimited repos, scans, and team members.
