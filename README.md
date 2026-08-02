# PainScout 🔍

Find **customer pain points** across public sources (Reddit, Hacker News, Stack Exchange,
GitHub issues, app stores), rank them by **buy intent**, and turn the best ones into
**launch-ready AI products** — complete project briefs, landing pages, and a searchable dashboard.

Built for vibe coders who want to solve real problems and get paid for it.

## How it works

1. **Scan** — pull complaints from Reddit, Hacker News (Algolia), Stack Exchange, GitHub issues,
   Google Play reviews and App Store reviews (free public APIs, no auth)
2. **Analyze** — an LLM (NVIDIA NIM / opencode zen / OpenAI) clusters complaints into pain themes,
   ranks them by opportunity score, and flags **buy intent** ("I'd pay for…")
3. **Fallback** — if no API key is set (or the LLM call fails), a heuristic keyword engine
   still produces a report with buy-intent detection
4. **Briefs** — the top opportunities become launch-ready **project briefs** (name, features,
   MVP scope, tech stack, build estimate, competitor gaps, WhatsApp bot spec) + standalone
   **landing pages** (self-contained HTML)
5. **Notify** — optionally send the report to Telegram
6. **Dashboard** — browse, search, filter and export everything in a local web UI

## Quick start

```bash
pip install -e ".[dev]"   # or: uv sync
painscout --query "wish there was a way to automate" --brief --telegram
painscout dashboard       # open the web dashboard at http://localhost:8791
```

### CLI options

```
-q, --query        search query              (env: PAINSCOUT_QUERY)
-s, --sources      reddit,hn,stackexchange,github,googleplay,appstore (default: all)
-l, --limit        max pain points/source    (env: PAINSCOUT_LIMIT)
-o, --out-dir      output directory          (default: reports/)
--app-id           App Store app id / Play package (env: PAINSCOUT_APP_ID)
--no-ai            force heuristic analyzer
--provider zen|nim|openai
--telegram         send report to Telegram
--brief            generate project briefs + landing pages for top opportunities
--brief-top N      how many briefs (default 3)
dashboard          subcommand: serve the web dashboard (--port, --no-browser)
```

## Configuration (env vars)

| Variable | Purpose |
|---|---|
| `OPENCODE_ZEN_API_KEY` | opencode zen key (fallback provider) |
| `NIM_API_KEY` | NVIDIA NIM key — **used automatically when set** (default provider) |
| `NIM_MODEL` | NVIDIA NIM model (default: `nvidia/nemotron-3-ultra-550b-a55b`) |
| `OPENAI_API_KEY` | OpenAI key |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Telegram chat id to deliver reports to |
| `PAINSCOUT_PROVIDER` | force `zen` / `nim` / `openai` |
| `PAINSCOUT_QUERY` | default search query |
| `PAINSCOUT_LIMIT` | default per-source limit |
| `PAINSCOUT_APP_ID` | App Store app id for reviews |
| `PAINSCOUT_OUT_DIR` | report output directory |

## GitHub Actions

- **CI** — runs on every push/PR: unit tests + ruff lint
- **Nightly scan** — every day at 06:00 UTC: runs a real scan, generates the top-3 project
  briefs + landing pages, commits everything to the repo, and sends the report to your Telegram.
  Trigger manually with *Actions → Nightly scan → Run workflow*.

## Tests

```bash
pytest                 # unit tests (fast, no network)
pytest -m e2e          # live tests against public APIs
```

## Example report

See `reports/latest.md` after the first scan — top opportunities with evidence quotes,
suggested AI solutions, pricing models, buy-intent flags, plus `reports/briefs/`
(project briefs) and `reports/landing/` (standalone HTML landing pages).
