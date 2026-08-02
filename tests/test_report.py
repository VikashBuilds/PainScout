"""Unit tests for report rendering and config."""

import json

from painscout.config import Settings
from painscout.models import Opportunity, PainPoint, Report
from painscout.report import render_json, render_markdown


def _report() -> Report:
    return Report(
        query="test query",
        pain_points=[
            PainPoint(source="reddit", title="t1", text="body1", url="u1"),
            PainPoint(source="hn", title="t2", text="body2", url="u2"),
        ],
        opportunities=[
            Opportunity(
                theme="Manual work",
                pain="People waste time.",
                evidence=["quote"],
                sources=["reddit"],
                url="u1",
                suggested_solution="AI bot",
                monetization="$29/mo",
                score=90.0,
            )
        ],
    )


def test_markdown_report_contains_sections():
    md = render_markdown(_report(), "ai")
    assert "# 🔍 PainScout Report" in md
    assert "**Query:** `test query`" in md
    assert "**Pain points scanned:** 2" in md
    assert "**Analyzer:** AI (LLM)" in md
    assert "### 1. [90/100] Manual work" in md
    assert "AI bot" in md
    assert "$29/mo" in md


def test_markdown_fallback_mode_label():
    md = render_markdown(_report(), "fallback")
    assert "heuristic fallback" in md


def test_json_report_roundtrip():
    data = json.loads(render_json(_report()))
    assert data["query"] == "test query"
    assert len(data["pain_points"]) == 2
    assert data["opportunities"][0]["score"] == 90.0


def test_settings_from_env_uses_defaults():
    s = Settings.from_env({})
    assert s.query == "wish there was a way to automate"
    assert s.limit_per_source == 15
    assert s.appstore_app_id == "310633997"


def test_settings_provider_priority():
    env = {"NIM_API_KEY": "nim", "OPENCODE_ZEN_API_KEY": "zen"}
    s = Settings.from_env(env)
    key, base, _model = s._provider_config()
    assert key == "nim"  # NIM wins when both present (default priority)


def test_settings_provider_override():
    env = {"NIM_API_KEY": "nim", "OPENCODE_ZEN_API_KEY": "zen", "PAINSCOUT_PROVIDER": "zen"}
    s = Settings.from_env(env)
    key, base, _model = s._provider_config()
    assert key == "zen"
    assert base == "https://opencode.ai/zen/v1"
