"""Pain point analysis — AI clustering with a keyword-based fallback.

The AI path calls any OpenAI-compatible /chat/completions endpoint
(opencode zen, NVIDIA NIM, OpenAI). If no API key is configured or the
call fails, we fall back to heuristic keyword clustering so the pipeline
always produces a report.
"""

from __future__ import annotations

import json
import re

import httpx

from painscout.config import Settings
from painscout.models import Opportunity, PainPoint

# --- Fallback keyword engine ---------------------------------------------

PAIN_KEYWORDS: list[tuple[str, float, list[str], str]] = [
    ("automation/manual work", 1.0, ["manual", "automate", "time-consuming", "tedious", "repetitive"],
     "AI workflow automation (Zapier-style, WhatsApp-first)"),
    ("customer support", 0.9, ["support", "refund", "agent", "unresponsive", "no reply"],
     "AI support agent / WhatsApp auto-responder"),
    ("billing/pricing", 0.9, ["price", "expensive", "overcharge", "billing", "subscription", "hidden fee"],
     "Price-comparison bot / billing-negotiation assistant"),
    ("bugs/quality", 0.8, ["bug", "broken", "crash", "glitch", "doesn't work", "error"],
     "QA automation / bug triage bot"),
    ("onboarding/usability", 0.8, ["confusing", "hard to use", "steep learning curve", "unclear", "setup"],
     "AI onboarding copilot / guided setup assistant"),
    ("data entry", 0.9, ["data entry", "typing", "copy paste", "spreadsheet", "excel", "csv"],
     "AI data-entry extractor (docs/screens -> structured data)"),
    ("communication/language", 0.7, ["translation", "language barrier", "english", "grammar"],
     "AI translation/rewriting bot (WhatsApp-first)"),
    ("scheduling/booking", 0.8, ["booking", "appointment", "scheduling", "no-show", "calendar"],
     "AI scheduling assistant with reminders (WhatsApp)"),
    ("scams/fraud", 0.9, ["scam", "fraud", "phishing", "fake", "chargeback"],
     "AI scam-detection / transaction-verification bot"),
    ("finding customers", 1.0, ["no customers", "leads", "traffic", "marketing", "sales", "grow"],
     "AI lead-gen / outreach automation"),
]

KEYWORD_REGEXES = {
    "score": re.compile(
        r"\b(horrible|terrible|awful|worst|hate|useless|waste|disappointed|frustrat\w*|annoy\w*"
        r"|nightmare|ridiculous|unacceptable|pathetic|never again|refund)\b",
        re.IGNORECASE,
    ),
    "wish": re.compile(r"\b(wish|if only|would be great if|should be able to|why (can't|cant))\b", re.IGNORECASE),
    # Buy-intent signals: someone willing to pay = monetizable pain.
    "buy": re.compile(
        r"\b(i('d| would| will)? pay|willing to (pay|spend)|take my money|would buy|"
        r"any (tool|app|bot|service) that|something that (can|could|would)|"
        r"there should be|someone should|please (make|build|fix|add)|"
        r"i'd love|i would love|worth (paying|it)|how much|subscription)\b",
        re.IGNORECASE,
    ),
}


def buy_intent_hits(text: str) -> int:
    """Count buy-intent signals in a pain point's text."""
    low = text.lower()
    hits = 0
    for pat in [
        r"pay",
        r"willing to (pay|spend)",
        r"take my money",
        r"would buy",
        r"subscription",
        r"worth paying",
        r"any tool",
        r"there should be",
        r"please (make|build|fix|add)",
    ]:
        if re.search(pat, low):
            hits += 1
    return hits


def _keyword_hits(text: str) -> list[tuple[str, float, list[str], str]]:
    hits = []
    low = text.lower()
    for theme, weight, words, solution in PAIN_KEYWORDS:
        if any(w in low for w in words):
            hits.append((theme, weight, words, solution))
    return hits


def fallback_analyze(points: list[PainPoint], top_n: int = 8) -> list[Opportunity]:
    """Cluster pain points by keyword theme; score by frequency + emotion."""
    buckets: dict[str, list[PainPoint]] = {}
    for p in points:
        hits = _keyword_hits(p.full_text)
        for theme, _w, _words, _sol in hits:
            buckets.setdefault(theme, []).append(p)
        if not hits and KEYWORD_REGEXES["score"].search(p.full_text):
            buckets.setdefault("general frustration", []).append(p)

    opportunities: list[Opportunity] = []
    for theme, group in buckets.items():
        solution = next((s for t, _w, _words, s in PAIN_KEYWORDS if t == theme), "AI-powered automation")
        emotion_bonus = sum(
            1 for p in group if KEYWORD_REGEXES["score"].search(p.full_text) or KEYWORD_REGEXES["wish"].search(p.full_text)
        )
        buy_bonus = sum(buy_intent_hits(p.full_text) for p in group)
        score = min(98.0, 20 + len(group) * 8 + emotion_bonus * 5 + buy_bonus * 6)
        evidence = [p.full_text[:220] for p in group[:4]]
        sources = sorted({p.source for p in group})
        best = max(group, key=lambda p: p.meta.get("score") or 0 if p.source != "appstore" else (p.meta.get("rating") or 0) * -1)
        opportunities.append(
            Opportunity(
                theme=theme,
                pain=f"Customers frequently complain about: {theme}.",
                evidence=evidence,
                sources=sources,
                url=best.url,
                suggested_solution=solution,
                monetization="SaaS subscription ($19-49/mo) or per-lead pricing via a WhatsApp bot",
                score=score,
                buy_intent=buy_bonus > 0,
            )
        )
    opportunities.sort(key=lambda o: o.score, reverse=True)
    return opportunities[:top_n]


# --- AI analyzer ----------------------------------------------------------

SYSTEM_PROMPT = """You are an AI market-research analyst for a solo developer ("vibe coder") who builds
AI SaaS products and WhatsApp automations. You are given raw customer complaints scraped from
Reddit, Hacker News, Stack Exchange, GitHub issues and app-store reviews.

Cluster the complaints into 3-6 distinct pain themes. For each theme, return a JSON object with:
- theme: short label (max 8 words)
- pain: what customers are suffering (1-2 sentences)
- evidence: 2-4 short verbatim quotes
- sources: list of source names
- url: the single best link
- suggested_solution: a concrete AI SaaS or WhatsApp automation that fixes this (1-2 sentences)
- monetization: how the solo dev could charge for it (pricing model)
- score: 0-100 opportunity score (frequency + emotion + willingness to pay)
- buy_intent: true only if customers literally say they'd pay / want to buy a fix
  ("I'd pay for", "willing to spend", "take my money", "any tool that", "please make")

Respond with ONLY a JSON object: {"opportunities": [ ... ]}."""


def ai_analyze(points: list[PainPoint], settings: Settings, top_n: int = 8) -> list[Opportunity]:
    """Run the LLM analysis. Returns [] on any failure — callers fall back."""
    global _last_ai_error
    key, base_url, model = settings._provider_config()
    if not key:
        _last_ai_error = "no API key configured"
        return []
    user_prompt = json.dumps(
        [
            {"source": p.source, "title": p.title, "text": p.text[:1200], "url": p.url, "meta": p.meta}
            for p in points
        ],
        ensure_ascii=False,
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        # Reasoning models (deepseek-v4, nemotron) burn tokens on
        # reasoning_content BEFORE producing content. 2500 was too small —
        # they'd hit finish_reason=length with an empty answer. 8000 gives
        # room for reasoning + a complete JSON response.
        "max_tokens": 8000,
    }
    try:
        with httpx.Client(timeout=180.0) as client:
            resp = client.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json=payload,
            )
            resp.raise_for_status()
            body = resp.json()
            content = body["choices"][0]["message"].get("content") or ""
            _last_ai_error = (
                f"empty content (finish_reason={body['choices'][0].get('finish_reason')})"
                if not content
                else ""
            )
        data = json.loads(_extract_json(content))
        opps = _opportunities_from_json(data, top_n)
        if not opps:
            _last_ai_error = "LLM returned no opportunities"
        return opps
    except (httpx.HTTPError, KeyError, json.JSONDecodeError, TypeError) as exc:
        _last_ai_error = f"{type(exc).__name__}: {exc}"
        return []


def last_ai_error() -> str:
    """Reason the last AI call failed (for diagnostics)."""
    return _last_ai_error


_last_ai_error = ""


def _extract_json(text: str) -> str:
    """Pull the first JSON object/array out of a model response."""
    text = text.strip()
    if text.startswith("{"):
        return text[: text.rfind("}") + 1] if text.rfind("}") >= 0 else text
    if text.startswith("["):
        return text[: text.rfind("]") + 1] if text.rfind("]") >= 0 else text
    m = re.search(r"\{.*\}", text, re.DOTALL)
    return m.group(0) if m else text


def _opportunities_from_json(data: dict, top_n: int) -> list[Opportunity]:
    items = data.get("opportunities", data if isinstance(data, list) else [])
    if not isinstance(items, list):
        return []
    opps = []
    for it in items:
        if not isinstance(it, dict):
            continue
        opps.append(
            Opportunity(
                theme=str(it.get("theme", "Unthemed")),
                pain=str(it.get("pain", "")),
                evidence=[str(e) for e in it.get("evidence", [])][:4],
                sources=[str(s) for s in it.get("sources", [])],
                url=str(it.get("url", "")),
                suggested_solution=str(it.get("suggested_solution", "")),
                monetization=str(it.get("monetization", "")),
                score=float(it.get("score", 50)),
                buy_intent=bool(it.get("buy_intent", False)),
            )
        )
    opps.sort(key=lambda o: o.score, reverse=True)
    return opps[:top_n]


def analyze(points: list[PainPoint], settings: Settings, top_n: int = 8) -> tuple[list[Opportunity], str]:
    """Run AI analysis; fall back to heuristics if unavailable/failed."""
    if settings.ai_enabled:
        ai_opps = ai_analyze(points, settings, top_n)
        if ai_opps:
            return ai_opps, "ai"
        print(f"   ⚠️  AI call failed ({last_ai_error()}) — using heuristic fallback")
    return fallback_analyze(points, top_n), "fallback"
