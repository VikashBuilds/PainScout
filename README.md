# PainScout 🔍

Find **customer pain points** across public sources (Reddit, Hacker News, App Store reviews),
then turn them into **monetizable AI project ideas** — AI SaaS products and WhatsApp automations.

Built for vibe coders who want to solve real problems and get paid for it.

## How it works

1. **Scan** — pull complaints from Reddit, Hacker News (Algolia API), Stack Exchange (free public
   API) and optionally App Store reviews (iTunes RSS)
2. **Analyze** — an LLM (opencode zen / NVIDIA NIM / OpenAI) clusters complaints into pain themes,
   ranks them by opportunity score, and suggests a concrete AI product + pricing model
3. **Fallback** — if no API key is set (or the LLM call fails), a heuristic keyword engine still produces a report
4. **Report** — Markdown + JSON saved to `reports/`
5. **Notify** — optionally send the report to Telegram

## Quick start

```bash
pip install -e ".[dev]"   # or: uv sync
painscout scan --query "wish there was a way to automate" --telegram
```

### CLI options

```
-q, --query        search query              (env: PAINSCOUT_QUERY)
-s, --sources      reddit,hn,appstore       (default: all)
-l, --limit        max pain points/source    (env: PAINSCOUT_LIMIT)
-o, --out-dir      output directory          (default: reports/)
--app-id           App Store app id          (env: PAINSCOUT_APP_ID)
--no-ai            force heuristic analyzer
--provider zen|nim|openai
--telegram         send report to Telegram
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
- **Nightly scan** — every day at 06:00 UTC: runs a real scan, commits the fresh
  report to the repo, and sends it to your Telegram. Trigger manually with
  *Actions → Nightly scan → Run workflow*.

## Tests

```bash
pytest                 # unit tests (fast, no network)
pytest -m e2e          # live tests against public APIs
```

## Example report

See `reports/latest.md` after the first scan — top opportunities with evidence
quotes, suggested AI solutions, and pricing models.
