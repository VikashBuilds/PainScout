"""Tests for the enhancement features: warehouse/trends, dedup, query bank,
watch list and market check."""

import json
from datetime import UTC, datetime, timedelta

from painscout.market import _classify, _keywords
from painscout.models import Opportunity, PainPoint, Report
from painscout.query_bank import DEFAULT_BANK, load_bank, pick_query
from painscout.warehouse import Store, dedup_points
from painscout.watch import parse_watch_apps


def _iso(days_ago: float) -> str:
    return (datetime.now(UTC) - timedelta(days=days_ago)).isoformat()


# --- Dedup (#2) ------------------------------------------------------------

def _make(url: str, source: str = "reddit", title: str = "t") -> PainPoint:
    return PainPoint(source=source, title=title, text="body", url=url)


def test_dedup_by_url():
    pts = [_make("https://x.com/a/1"), _make("https://x.com/a/1"), _make("https://x.com/b/2"), _make("")]
    unique, dropped = dedup_points(pts)
    assert dropped == 1
    assert len(unique) == 3


def test_dedup_by_title_fallback_when_no_url():
    pts = [
        PainPoint(source="hn", title="Same title", text="one", url=""),
        PainPoint(source="hn", title="same title", text="two", url=""),
    ]
    unique, dropped = dedup_points(pts)
    assert dropped == 1
    assert len(unique) == 1


# --- Warehouse / trends (#2 + #5) -------------------------------------------

def _opp(theme: str, score: float = 70.0) -> Opportunity:
    return Opportunity(
        theme=theme, pain="x", evidence=["quote"], sources=["hn"], url="u",
        suggested_solution="s", monetization="$9", score=score,
    )


def _report(query: str, gen: str, opps: list) -> Report:
    return Report(
        query=query,
        generated_at=gen,
        pain_points=[_make("https://x/1")],
        opportunities=opps,
    )


def test_store_roundtrip_and_classify(tmp_path):
    db = tmp_path / "h.db"
    store = Store(db)
    store.record(_report("q", _iso(0), [_opp("Manual invoicing")]), "ai")
    t = store.theme_trends()
    assert "Manual invoicing" in t
    assert t["Manual invoicing"]["scans"] == 1
    assert store.classify(t["Manual invoicing"]) in ("new", "rising", "hot", "dormant", "flat", "stable", "cooling")
    store.close()


def test_store_rising_classification(tmp_path):
    db = tmp_path / "h.db"
    store = Store(db)
    # One appearance ~20 days ago, two appearances in the last 7 days -> rising
    store.record(_report("q", _iso(20), [_opp("Automation X")]), "ai")
    store.record(_report("q", _iso(2), [_opp("Automation X")]), "ai")
    store.record(_report("q", _iso(1), [_opp("Automation X")]), "ai")
    t = store.theme_trends()["Automation X"]
    assert t["last7"] == 2
    assert t["prev7"] == 0
    assert store.classify(t) == "rising"
    store.close()


def test_store_handles_list_text(tmp_path):
    """Some sources return text as a list — must not break persistence."""
    db = tmp_path / "h.db"
    store = Store(db)
    pp = PainPoint(source="hn", title="t", text=["line one", "line two"], url="https://x", created_at="t")
    r = Report(query="q", pain_points=[pp], opportunities=[_opp("Anything")])
    store.record(r, "ai")
    import sqlite3

    con = sqlite3.connect(db)
    row = con.execute("SELECT text FROM pain_points").fetchone()
    assert row[0] == "line one line two"
    store.close()


def test_history_json_artifacts(tmp_path):
    from painscout.warehouse import write_history_artifacts

    db = tmp_path / "h.db"
    store = Store(db)
    store.record(_report("q", _iso(0), [_opp("Theme A"), _opp("Theme B", 90)]), "ai")
    hj, tcsv = write_history_artifacts(store, tmp_path / "reports")
    data = json.loads(hj.read_text())
    assert data["theme_count"] == 2
    assert {t["theme"] for t in data["themes"]} == {"Theme A", "Theme B"}
    csv = tcsv.read_text()
    assert "theme,trend,occurrences,scans,avg_score" in csv
    assert "Theme A" in csv
    store.close()


# --- Query bank (#3) ---------------------------------------------------------

def test_pick_query_deterministic():
    from datetime import date

    q1, i1 = pick_query(day=date(2026, 8, 3))
    q2, i2 = pick_query(day=date(2026, 8, 3))
    assert q1 == q2 and i1 == i2
    assert q1 in DEFAULT_BANK


def test_pick_query_rotates():
    from datetime import date

    a, ia = pick_query(day=date(2026, 8, 3))
    b, ib = pick_query(day=date(2026, 8, 4))
    assert ia != ib or a != b  # different days pick different slots


def test_custom_bank_from_env(monkeypatch):
    from datetime import date

    monkeypatch.setenv("PAINSCOUT_QUERY_BANK", json.dumps(["niche one", "niche two"]))
    bank = load_bank()
    assert bank == ["niche one", "niche two"]
    q, i = pick_query(index=1, day=date(2026, 8, 3))
    assert q == "niche two"


# --- Watch list (#6) ---------------------------------------------------------

def test_parse_watch_apps_default_empty(monkeypatch):
    monkeypatch.delenv("PAINSCOUT_WATCH_APPS", raising=False)
    assert parse_watch_apps("") == []


def test_parse_watch_apps_mixed():
    raw = "ios:310633997|WhatsApp, android:com.whatsapp"
    apps = parse_watch_apps(raw)
    assert apps[0] == {"platform": "ios", "id": "310633997", "name": "WhatsApp"}
    assert apps[1] == {"platform": "android", "id": "com.whatsapp", "name": ""}


def test_parse_watch_apps_bare_id_is_ios():
    apps = parse_watch_apps("310633997")
    assert apps[0]["platform"] == "ios"
    assert apps[0]["id"] == "310633997"


def test_parse_watch_apps_env(monkeypatch):
    monkeypatch.setenv("PAINSCOUT_WATCH_APPS", "ios:1|A, android:com.b")
    apps = parse_watch_apps()
    assert len(apps) == 2


# --- Market check (#4) -------------------------------------------------------

def test_keywords_derivation():
    assert _keywords("Billing confusion in SaaS tools") == "billing confusion saas"
    assert _keywords("")  # never raises


def test_market_classify_levels():
    low = _classify("query", [{"name": "r1", "stars": 10, "url": "u1"}], hn_hits=2)
    assert low.level == "low"
    med = _classify("query", [{"name": "r1", "stars": 50, "url": "u1"},
                              {"name": "r2", "stars": 40, "url": "u2"},
                              {"name": "r3", "stars": 30, "url": "u3"}], hn_hits=10)
    assert med.level == "medium"
    big = _classify("query", [{"name": f"r{i}", "stars": 5000, "url": f"u{i}"} for i in range(3)], hn_hits=50)
    assert big.level == "high"
    assert big.note and "differentiation" in big.note


def test_market_result_dict_shape():
    r = _classify("query", [{"name": "repo", "stars": 5, "url": "https://g/r"}], hn_hits=3)
    d = r.to_dict()
    assert set(d) == {"level", "existing", "links", "hn_hits", "note"}
    assert d["existing"] == ["repo (★5)"]
    assert d["links"] == ["https://g/r"]


# --- Report surfaces trend/market (#2/#4 in output) ---------------------------

def test_report_markdown_shows_trend_and_market():
    from painscout.report import render_markdown

    opp = _opp("Trendy theme")
    opp.trend = "rising"
    opp.market = {"level": "medium", "existing": ["comp (★10)"], "note": "Room to differentiate."}
    r = Report(query="q", pain_points=[_make("https://x/1")], opportunities=[opp])
    md = render_markdown(r, "ai")
    assert "rising" in md
    assert "**Competition:** MEDIUM" in md
    assert "comp (★10)" in md


def test_opportunity_to_dict_omits_empty_extras():
    opp = _opp("plain")
    d = opp.to_dict()
    assert "trend" not in d and "market" not in d
