"""End-to-end test: live scan against public APIs (needs network).

Run with: pytest -m e2e
Skips gracefully when offline.
"""

import pytest

from painscout.analyzer import fallback_analyze
from painscout.config import Settings
from painscout.models import Report
from painscout.report import render_markdown
from painscout.sources import get_sources

pytestmark = pytest.mark.e2e


def test_live_hn_scan():
    from painscout.sources.hackernews import HackerNewsSource

    src = HackerNewsSource(Settings(limit_per_source=5))
    try:
        points = src.fetch("customer support is terrible", 5)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"HN API unreachable: {exc}")
    assert len(points) > 0
    assert all(p.source == "hackernews" for p in points)
    assert all(p.url.startswith("https://news.ycombinator.com") for p in points)


def test_live_appstore_scan():
    from painscout.sources.appstore import AppStoreSource

    src = AppStoreSource(Settings(limit_per_source=5))
    try:
        points = src.fetch("", 5)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"iTunes API unreachable: {exc}")
    if not points:
        pytest.skip("iTunes returned no reviews (Apple has been sunsetting this feed)")

    assert all(p.source == "appstore" for p in points)
    assert all("rating" in p.meta for p in points)


def test_live_stackexchange_scan():
    from painscout.sources.stackexchange import StackExchangeSource

    src = StackExchangeSource(Settings(limit_per_source=5))
    try:
        points = src.fetch("automate manual data entry", 5)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Stack Exchange API unreachable: {exc}")
    assert len(points) > 0
    assert all(p.source == "stackexchange" for p in points)
    assert all(p.url.startswith("https://") for p in points)


def test_live_reddit_scan():
    from painscout.sources.reddit import RedditSource

    src = RedditSource(Settings(limit_per_source=3))
    try:
        points = src.fetch("billing is confusing", 3)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Reddit API unreachable: {exc}")
    # Reddit may block datacenter IPs; allow empty but don't fail the suite.
    if points:
        assert all(p.source == "reddit" for p in points)


def test_full_pipeline_no_ai():
    """The whole pipeline without AI: scan -> analyze -> report."""
    settings = Settings(limit_per_source=5)
    points: list = []
    for src in get_sources(settings):
        try:
            points.extend(src.fetch(settings.query, settings.limit_per_source))
        except Exception:  # noqa: BLE001
            continue
    if not points:
        pytest.skip("No data collected from any source — network restricted")
    opps = fallback_analyze(points, top_n=5)
    report = Report(query=settings.query, pain_points=points, opportunities=opps)
    md = render_markdown(report, "fallback")
    assert "# 🔍 PainScout Report" in md
    assert f"**Pain points scanned:** {len(points)}" in md
