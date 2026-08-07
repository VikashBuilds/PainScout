# 🚀 ArchGuard

*Enforce architectural intent while AI codes fast*

## The problem
AI coding agents generate code faster than developers can review, eroding architectural boundaries and creating unreviewed technical debt that no one understands.

## The solution
ArchGuard sits between AI agents and your codebase as a real-time architectural gatekeeper. It enforces your structural rules, requires human sign-off on risky changes, and maintains a living architecture decision log so team understanding scales with AI velocity.

## Features (v1)
- Architectural rule engine (YAML-defined layer boundaries, dependency direction, naming conventions)
- Human-in-the-loop gates: block AI file creation, public API changes, DB migrations until approved
- Auto-generated Architecture Decision Records linked to PRs and AI prompts
- Code ownership heatmap: tracks who reviewed what, flags modules only AI has touched
- AI watermarking: labels AI vs human code, tracks review status per hunk
- Technical debt dashboard: visualizes gate bypasses, review backlog aging, drift trends
- Context injection: syncs your rules to .cursorrules/.github/copilot-instructions automatically
- Refactoring guardrails: prevents architectural drift during AI-assisted large-scale edits
- Team knowledge bus-factor report: identifies onboarding gaps before they hurt
- Review velocity metrics: compares AI-generated vs human-reviewed throughput

## MVP scope
VS Code extension that intercepts file creates/edits from Cursor/Copilot, validates against a YAML rule set (layers, deps, naming), blocks or flags violations with inline diagnostics, writes ADR entries to .archguard/adrs/, and syncs rules to .cursorrules. Local-first, no backend required.

## Tech stack
VS Code Extension API (TypeScript), Tree-sitter WASM for multi-language AST parsing, SQLite (better-sqlite3) for local ADR/event store, YAML (js-yaml) for rule configuration, GitHub API (Octokit) for PR linking, Cursor/Copilot chat API hooks (where exposed), Bun for fast test/dev loop, Vitest + Playwright for extension testing

## Build estimate: 21 days

## Competitors & gaps
- **Cursor** — gap: Generates code but has no architectural enforcement or review gates
- **GitHub Copilot** — gap: No codebase-wide architectural awareness; only local context
- **SonarQube** — gap: Retrospective code smell detection, not preventive architectural gates
- **ArchUnit** — gap: Java-only, test-time only, not integrated with AI workflows
- **CodeClimate** — gap: Post-merge analysis; doesn't stop bad AI code at the source

## Landing page copy
- **Headline:** Stop AI from Architecting Your Codebase Into a Mess
- **Subheadline:** ArchGuard enforces your architectural decisions while AI codes — so you stay in control without slowing down.
- Bullet: Block AI-generated code that violates layer boundaries
- Bullet: Auto-generate Architecture Decision Records for every structural change
- Bullet: See exactly which modules only AI understands — before it's too late
- Bullet: Inject your architecture into Cursor/Copilot so they code *your* way
- **CTA:** Add to VS Code Free

## WhatsApp-first bot
- **Flow:** Dev gets WhatsApp alert when AI tries to create files violating architecture rules. Reply 'APPROVE' or 'BLOCK' to gate the change from phone.
- **Commands:** STATUS, RULES, APPROVE <gate_id>, BLOCK <gate_id>, DEBT, OWNERSHIP
- **Pricing:** Included in Pro/Team plans. Free tier: 5 gates/day via WhatsApp.

## Pricing model: $15/mo per dev (Pro), $40/mo per seat (Team), free tier: 5 rules, 10 gates/day, local-only
