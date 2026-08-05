# 🚀 FlowLens

*Catch silent n8n failures before they waste your debugging hours*

## The problem
n8n power-users lose hours daily to silent expression failures that resolve to null without errors, logs, or failed node indicators — plus fragmented UX across AI tools like missing shortcuts, split billing, and manual refreshes.

## The solution
FlowLens wraps n8n with a real-time observability layer that instruments every expression evaluation, surfaces silent null resolutions instantly, and adds a unified command palette for cross-tool shortcuts, billing views, and auto-refresh — all without modifying existing workflows.

## Features (v1)
- Expression-level trace panel showing every evaluation result, type, and null/undefined resolution in real-time
- Silent-failure alerts via in-app toast, webhook, or WhatsApp when any expression resolves to null/undefined unexpectedly
- Unified command palette (Cmd+K) with shortcuts to n8n credentials, executions, workflows, and external AI tool dashboards (OpenAI, Anthropic, etc.)
- Auto-refresh toggle for execution lists and workflow editor with configurable intervals
- Consolidated billing dashboard pulling spend from OpenAI, Anthropic, Replicate, and n8n cloud via API keys
- URL canonicalizer that rewrites confusing n8n execution URLs to human-readable paths (workflow-name/execution-id)
- One-click 'Re-run from failed expression' that isolates and re-executes only the problematic node chain
- Expression playground sidebar to test any expression against live execution context before deploying
- Whisper-mode logging: captures all expression evaluations without cluttering n8n's native logs
- Team sharable debug links with time-limited access for pair-debugging silent failures

## MVP scope
Build a Chrome extension that injects into n8n cloud/self-hosted, intercepts expression evaluations via monkey-patched Function constructor, displays trace panel in a docked sidebar, and ships the command palette with 5 core shortcuts (credentials, executions, workflows, OpenAI billing, Anthropic billing). No backend required — all client-side.

## Tech stack
Manifest V3 Chrome Extension (TypeScript), React 18 + Tailwind CSS for sidebar UI, Vite for build + HMR, n8n REST API (self-hosted & cloud) for execution/workflow data, OpenAI/Anthropic/Replicate billing APIs (user-provided keys, stored locally), IndexedDB (via idb) for local trace storage, Vercel for landing page + static asset hosting, Playwright for E2E testing against n8n demo instance

## Build estimate: 21 days

## Competitors & gaps
- **n8n native debug panel** — gap: Only shows node I/O, not expression-level evaluation; silent nulls invisible
- **Datadog APM** — gap: Overkill, expensive, doesn't understand n8n expression semantics or paired-item resolution
- **Sentry** — gap: Catches thrown errors, not silent null resolutions; no n8n-specific context
- **Postman** — gap: API testing only, no workflow execution observability
- **Custom console.log spam** — gap: Manual, pollutes logs, no history, no alerts, no cross-tool shortcuts

## Landing page copy
- **Headline:** Stop guessing why your n8n workflow returned null
- **Subheadline:** FlowLens shows every expression evaluation in real-time, alerts on silent failures, and gives you the shortcuts n8n forgot — all in a lightweight sidebar.
- Bullet: See every expression result, type, and null resolution as it happens
- Bullet: Get alerted the moment a paired-item lookup silently returns undefined
- Bullet: Jump to credentials, executions, or OpenAI billing with Cmd+K
- Bullet: Auto-refresh execution lists — no more F5 mashing
- Bullet: One-click re-run from the exact expression that failed silently
- Bullet: Works on n8n Cloud and self-hosted, zero server setup
- **CTA:** Install Free Chrome Extension

## WhatsApp-first bot
- **Flow:** User links n8n instance via /connect command → bot stores webhook URL → on every execution, n8n calls webhook → bot evaluates expressions against stored context → if silent null detected, sends WhatsApp alert with workflow name, node, expression, and deep link to FlowLens trace. User replies 'retry' to trigger re-run from that node.
- **Commands:** /connect <n8n_webhook_url> — link your n8n instance, /trace <execution_id> — get last 50 expression evaluations for that run, /alerts on|off — toggle silent-failure notifications, /billing — show consolidated AI spend (OpenAI, Anthropic, Replicate), /shortcuts — list all Cmd+K shortcuts available in extension, /retry <execution_id> <node_name> — re-run workflow from specific node
- **Pricing:** Free tier: 100 executions/mo alerts. Pro: $12/mo unlimited alerts, billing dashboard, team debug links. WhatsApp bot included in Pro.

## Pricing model: Freemium Chrome extension: Free (100 traced executions/mo, basic sidebar). Pro $12/mo (unlimited traces, alerts, billing dashboard, team debug links, WhatsApp bot). Team $35/mo (5 seats, shared traces, SSO).
