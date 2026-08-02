"""Tests for new sources, buy-intent scoring, briefs and landing pages."""

from painscout.analyzer import buy_intent_hits, fallback_analyze
from painscout.brief import _template_brief, render_brief_markdown
from painscout.landing import render_landing_page
from painscout.models import Opportunity, PainPoint
from painscout.sources.github import GitHubIssuesSource
from painscout.sources.googleplay import GooglePlaySource

# --- GitHub source ---------------------------------------------------------

def test_github_parse():
    data = {
        "items": [
            {
                "title": "Please add automation for bulk imports",
                "body": "We waste hours on this every week. Any tool that does this would be amazing.",
                "html_url": "https://github.com/n8n-io/n8n/issues/123",
                "created_at": "2026-01-01T00:00:00Z",
                "comments": 12,
                "reactions": {"+1": 45},
                "repository_url": "https://api.github.com/repos/n8n-io/n8n",
            },
            {"title": "", "body": "no title"},
        ]
    }
    points = GitHubIssuesSource._parse(data, repo="n8n-io/n8n")
    assert len(points) == 1
    assert points[0].source == "github"
    assert points[0].url == "https://github.com/n8n-io/n8n/issues/123"
    assert points[0].meta["reactions"] == 45
    assert points[0].meta["repo"] == "n8n-io/n8n"


def test_github_parse_empty():
    assert GitHubIssuesSource._parse({"items": []}) == []


# --- Google Play source ----------------------------------------------------

def test_googleplay_parse_blocked_page():
    # Cloudflare/error pages return no points (graceful degradation)
    assert GooglePlaySource._parse("<html>Error 405</html>") == []


def test_googleplay_parse_empty():
    assert GooglePlaySource._parse("") == []


def test_googleplay_parse_valid_blob():
    import json

    review = {
        "text": "This app charged me twice!\nSupport never replies.",
        "starRating": 1,
        "url": "https://play.google.com/store/apps/details?id=com.whatsapp&reviewId=1",
        "timestamp": {"iso": "2026-02-01T00:00:00Z"},
        "appId": "com.whatsapp",
    }
    # Real responses wrap each review as an escaped JSON string inside the blob.
    raw = ")]}' [[" + json.dumps(json.dumps(review)) + "],null]"
    points = GooglePlaySource._parse(raw)
    assert len(points) == 1
    assert points[0].source == "googleplay"
    assert points[0].meta["rating"] == 1


# --- Buy-intent scoring ----------------------------------------------------

def test_buy_intent_hits():
    assert buy_intent_hits("I would pay for a tool that does this") >= 1
    assert buy_intent_hits("willing to spend $50 on anything that fixes this") >= 1
    assert buy_intent_hits("please build this, take my money") >= 1
    assert buy_intent_hits("this app is fine, no complaints") == 0


def test_buy_intent_boosts_fallback_score():
    points = [
        PainPoint(
            source="reddit",
            title="Manual invoicing is killing me",
            text="I would literally pay for a tool that automates this. Any tool that works.",
            url="https://x/1",
        ),
        PainPoint(
            source="hn",
            title="Same pain, no money talk",
            text="Manual invoicing is slow and tedious.",
            url="https://x/2",
        ),
    ]
    opps = fallback_analyze(points)
    assert opps
    top = opps[0]
    assert top.buy_intent is True
    assert top.score >= 20 + 2 * 8  # baseline + buy bonus


# --- Project briefs ---------------------------------------------------------

def _sample_opp() -> Opportunity:
    return Opportunity(
        theme="Manual invoicing",
        pain="Small businesses waste hours on invoices.",
        evidence=["quote"],
        sources=["reddit"],
        url="https://x/1",
        suggested_solution="AI invoice extractor bot",
        monetization="$29/mo",
        score=80,
        buy_intent=True,
    )


def test_template_brief_fields():
    brief = _template_brief(_sample_opp())
    assert brief.name
    assert brief.tagline
    assert brief.features
    assert brief.mvp_scope
    assert brief.tech_stack
    assert 1 <= brief.build_estimate_days <= 30
    assert brief.competitors
    assert brief.landing_copy.get("headline")
    assert brief.whatsapp_bot.get("flow")
    assert brief.pricing_model == "$29/mo"


def test_template_brief_slug():
    brief = _template_brief(_sample_opp())
    assert brief.slug and " " not in brief.slug


def test_brief_markdown_sections():
    brief = _template_brief(_sample_opp())
    md = render_brief_markdown(brief)
    assert "# 🚀" in md
    assert "## The problem" in md
    assert "## Features (v1)" in md
    assert "## MVP scope" in md
    assert "## Competitors & gaps" in md
    assert "## WhatsApp-first bot" in md


def test_brief_from_ai_json():
    from painscout.brief import _brief_from_json

    data = {
        "name": "InvoiceBot",
        "tagline": "Invoices on autopilot",
        "problem": "Manual invoicing sucks.",
        "solution": "AI extracts invoices from email.",
        "features": ["f1", "f2"],
        "mvp_scope": "WhatsApp bot + LLM",
        "tech_stack": ["Python", "FastAPI"],
        "build_estimate_days": 10,
        "competitors": [{"name": "Xero", "gap": "No AI"}],
        "landing_copy": {"headline": "H", "bullets": ["b1"]},
        "whatsapp_bot": {"flow": "f", "commands": ["/start"]},
        "pricing_model": "$49/mo",
    }
    brief = _brief_from_json(data, _sample_opp())
    assert brief.name == "InvoiceBot"
    assert brief.build_estimate_days == 10
    assert brief.landing_copy["headline"] == "H"
    assert brief.pricing_model == "$49/mo"


# --- Landing pages ----------------------------------------------------------

def test_landing_page_renders():
    brief = _template_brief(_sample_opp())
    html = render_landing_page(brief)
    assert "<!DOCTYPE html>" in html
    assert "<title>" in html
    assert "WhatsApp" in html
    assert "inline" not in html.split("<style>")[0]  # CSS is embedded
    assert html.count("</html>") == 1
