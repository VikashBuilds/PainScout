"""Idea-to-launch: turn an Opportunity into a build-ready project brief.

The AI (NIM/zen/OpenAI) expands an opportunity into a full brief: product
name, feature list, MVP scope, tech stack, build estimate, competitor gap
analysis, landing-page copy and a WhatsApp bot spec. A template-based
fallback kicks in when no API key is available.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import httpx

from painscout.analyzer import _extract_json, last_ai_error
from painscout.config import Settings
from painscout.models import Opportunity

BRIEF_SYSTEM_PROMPT = """You are a product strategist for a solo developer ("vibe coder") who builds AI SaaS
products and WhatsApp automations. Given ONE validated customer pain point, design a
launch-ready product. Return ONLY a JSON object with exactly these keys:
- name: catchy product name (max 3 words)
- tagline: one-line value prop (max 15 words)
- problem: restate the pain crisply (1-2 sentences)
- solution: how the product fixes it (2-3 sentences)
- features: array of 6-10 concrete features for v1
- mvp_scope: what to build first, minimal viable version (2-3 sentences)
- tech_stack: array of 4-8 recommended technologies (be specific: framework, AI APIs, hosting)
- build_estimate_days: integer estimate for a solo dev to ship the MVP
- competitors: array of {"name": str, "gap": str} — 3-5 existing products and the gap they leave
- landing_copy: {"headline": str, "subheadline": str, "bullets": [str], "cta": str}
- whatsapp_bot: {"flow": str, "commands": [str], "pricing": str} — how a WhatsApp-first version works
- pricing_model: str (e.g. "$29/mo SaaS, freemium, per-lead")
Be concrete and specific. No filler."""


@dataclass
class ProjectBrief:
    opportunity_theme: str
    name: str = ""
    tagline: str = ""
    problem: str = ""
    solution: str = ""
    features: list[str] = field(default_factory=list)
    mvp_scope: str = ""
    tech_stack: list[str] = field(default_factory=list)
    build_estimate_days: int = 14
    competitors: list[dict] = field(default_factory=list)
    landing_copy: dict = field(default_factory=dict)
    whatsapp_bot: dict = field(default_factory=dict)
    pricing_model: str = ""

    def to_dict(self) -> dict:
        return {
            "opportunity_theme": self.opportunity_theme,
            "name": self.name,
            "tagline": self.tagline,
            "problem": self.problem,
            "solution": self.solution,
            "features": self.features,
            "mvp_scope": self.mvp_scope,
            "tech_stack": self.tech_stack,
            "build_estimate_days": self.build_estimate_days,
            "competitors": self.competitors,
            "landing_copy": self.landing_copy,
            "whatsapp_bot": self.whatsapp_bot,
            "pricing_model": self.pricing_model,
        }

    @property
    def slug(self) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
        return slug or "opportunity"


def generate_brief(opp: Opportunity, settings: Settings) -> tuple[ProjectBrief, str]:
    """Generate a project brief; fall back to a template when AI is unavailable."""
    key, base_url, model = settings._provider_config()
    if key:
        brief = _ai_brief(opp, key, base_url, model)
        if brief:
            return brief, "ai"
    return _template_brief(opp), "template"


def _ai_brief(opp: Opportunity, key: str, base_url: str, model: str) -> ProjectBrief | None:
    user_prompt = json.dumps(
        {
            "theme": opp.theme,
            "pain": opp.pain,
            "evidence": opp.evidence[:3],
            "url": opp.url,
            "buy_intent": opp.buy_intent,
        },
        ensure_ascii=False,
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": BRIEF_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 8000,  # reasoning models burn tokens before content
    }
    try:
        with httpx.Client(timeout=180.0) as client:
            resp = client.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json=payload,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"].get("content") or ""
        if not content:
            return None
        data = json.loads(_extract_json(content))
        return _brief_from_json(data, opp)
    except (httpx.HTTPError, KeyError, json.JSONDecodeError, TypeError):
        return None


def _brief_from_json(data: dict, opp: Opportunity) -> ProjectBrief:
    landing = data.get("landing_copy") or {}
    wa = data.get("whatsapp_bot") or {}
    return ProjectBrief(
        opportunity_theme=opp.theme,
        name=str(data.get("name") or opp.theme),
        tagline=str(data.get("tagline") or ""),
        problem=str(data.get("problem") or opp.pain),
        solution=str(data.get("solution") or opp.suggested_solution),
        features=[str(f) for f in data.get("features", [])],
        mvp_scope=str(data.get("mvp_scope") or ""),
        tech_stack=[str(t) for t in data.get("tech_stack", [])],
        build_estimate_days=int(data.get("build_estimate_days") or 14),
        competitors=[{str(k): str(v) for k, v in c.items()} for c in data.get("competitors", []) if isinstance(c, dict)],
        landing_copy=_stringify_dict(landing),
        whatsapp_bot=_stringify_dict(wa),
        pricing_model=str(data.get("pricing_model") or opp.monetization),
    )


def _stringify_dict(d: dict) -> dict:
    """Keep list values as lists (bullets, commands) but stringify scalars."""
    out: dict = {}
    for k, v in d.items():
        if isinstance(v, list):
            out[str(k)] = [str(i) for i in v]
        elif isinstance(v, dict):
            out[str(k)] = {str(kk): str(vv) for kk, vv in v.items()}
        else:
            out[str(k)] = str(v)
    return out


def _template_brief(opp: Opportunity) -> ProjectBrief:
    """Deterministic fallback brief built from the opportunity fields."""
    wa_flow = (
        f"User texts the bot a description of their problem -> bot asks 3 clarifying questions -> "
        f"bot proposes {opp.suggested_solution} and a price -> user confirms in chat -> "
        f"bot delivers the result (report/automation) and collects payment via a payment link."
    )
    return ProjectBrief(
        opportunity_theme=opp.theme,
        name=_slugify_name(opp.theme),
        tagline=f"Fix {opp.theme.lower()} with AI — no code, no consultants.",
        problem=opp.pain,
        solution=opp.suggested_solution,
        features=[
            f"AI-powered {opp.theme.lower()} assistant",
            "Instant WhatsApp / web chat interface",
            "Auto-generated reports & summaries",
            "Payment collection via payment link",
            "Human handoff when needed",
        ],
        mvp_scope=f"Build a WhatsApp bot that takes a user's {opp.theme.lower()} description, "
        f"runs it through an LLM, and returns a structured result with a payment link.",
        tech_stack=["Python", "FastAPI", "OpenAI-compatible LLM API", "WhatsApp Business API", "Stripe"],
        build_estimate_days=7,
        competitors=[
            {"name": "Generic no-code tools (Zapier, Make)", "gap": "No AI understanding of the actual problem"},
            {"name": "Human consultants/agencies", "gap": "Slow, expensive, not available 24/7"},
        ],
        landing_copy={
            "headline": f"Stop suffering from {opp.theme.lower()}",
            "subheadline": opp.suggested_solution,
            "bullets": ["Works on WhatsApp — no new apps", "AI-powered, results in minutes", "Pay only when it works"],
            "cta": "Start on WhatsApp",
        },
        whatsapp_bot={
            "flow": wa_flow,
            "commands": ["/start", "/demo", "/pricing", "/status"],
            "pricing": opp.monetization,
        },
        pricing_model=opp.monetization,
    )


def _slugify_name(theme: str) -> str:
    words = re.sub(r"[^a-z0-9 ]", "", theme.lower()).split()
    return "".join(w.capitalize() for w in words[:3]) or "PainFix"


def render_brief_markdown(brief: ProjectBrief) -> str:
    lines = [
        f"# 🚀 {brief.name}",
        "",
        f"*{brief.tagline}*",
        "",
        "## The problem",
        brief.problem,
        "",
        "## The solution",
        brief.solution,
        "",
        "## Features (v1)",
    ]
    lines += [f"- {f}" for f in brief.features] or ["- TBD"]
    lines += [
        "",
        "## MVP scope",
        brief.mvp_scope,
        "",
        "## Tech stack",
        ", ".join(brief.tech_stack) if brief.tech_stack else "TBD",
        "",
        f"## Build estimate: {brief.build_estimate_days} days",
        "",
        "## Competitors & gaps",
    ]
    lines += [f"- **{c.get('name', '?')}** — gap: {c.get('gap', '?')}" for c in brief.competitors] or ["- TBD"]
    lines += [
        "",
        "## Landing page copy",
    ]
    lc = brief.landing_copy
    if lc:
        bullets = lc.get("bullets", [])
        if isinstance(bullets, str):
            bullets = [bullets]
        lines += [
            f"- **Headline:** {lc.get('headline', '')}",
            f"- **Subheadline:** {lc.get('subheadline', '')}",
        ]
        lines += [f"- Bullet: {b}" for b in bullets]
        lines += [f"- **CTA:** {lc.get('cta', '')}"]
    lines += [
        "",
        "## WhatsApp-first bot",
    ]
    wa = brief.whatsapp_bot
    if wa:
        cmds = wa.get("commands", [])
        if isinstance(cmds, str):
            cmds = [cmds]
        lines += [
            f"- **Flow:** {wa.get('flow', '')}",
            f"- **Commands:** {', '.join(cmds)}",
            f"- **Pricing:** {wa.get('pricing', '')}",
        ]
    lines += ["", f"## Pricing model: {brief.pricing_model}", ""]
    return "\n".join(lines)


def save_brief(brief: ProjectBrief, out_dir: Path) -> Path:
    out_dir = out_dir / "briefs"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{brief.slug}.md"
    path.write_text(render_brief_markdown(brief), encoding="utf-8")
    (out_dir / f"{brief.slug}.json").write_text(json.dumps(brief.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def last_brief_error() -> str:
    return last_ai_error()
