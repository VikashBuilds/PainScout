"""Tests for the web dashboard endpoints."""

import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from painscout.dashboard import _PAGE, _briefs_index, _load_report
from painscout.models import Opportunity, PainPoint, Report


@pytest.fixture()
def report_dir(tmp_path: Path) -> Path:
    report = Report(
        query="test",
        pain_points=[
            PainPoint(source="reddit", title="t", text="body", url="u"),
            PainPoint(source="hn", title="t2", text="body2", url="u2"),
        ],
        opportunities=[
            Opportunity(
                theme="Manual work",
                pain="People waste time.",
                evidence=["e1"],
                sources=["reddit", "hn"],
                url="u1",
                suggested_solution="AI bot",
                monetization="$29/mo",
                score=90,
                buy_intent=True,
            )
        ],
    )
    (tmp_path / "latest.json").write_text(json.dumps(report.to_dict()), encoding="utf-8")
    return tmp_path


def test_load_report(report_dir: Path):
    report = _load_report(report_dir)
    assert len(report.opportunities) == 1
    assert report.opportunities[0].buy_intent is True
    assert len(report.pain_points) == 2


def test_briefs_index_empty(report_dir: Path):
    assert _briefs_index(report_dir) == {}


def test_briefs_index_with_brief(report_dir: Path):
    (report_dir / "briefs").mkdir()
    (report_dir / "briefs" / "TestBot.json").write_text(
        json.dumps({"name": "TestBot", "tagline": "tg", "build_estimate_days": 7}),
        encoding="utf-8",
    )
    briefs = _briefs_index(report_dir)
    assert "TestBot" in briefs
    assert briefs["TestBot"].build_estimate_days == 7


def test_dashboard_page_has_core_ui():
    assert "PainScout" in _PAGE
    assert "buy_intent" in _PAGE
    assert "exportCsv" in _PAGE
    assert "/api/report" in _PAGE


def test_static_dashboard_is_fetch_based():
    from painscout.static_dashboard import render_static_dashboard

    html = render_static_dashboard()
    # Static version must not depend on the local server API
    assert "/api/report" not in html
    assert "fetch('reports/latest.json')" in html
    assert "fetch('reports/briefs/index.json')" in html
    assert "Launch-ready project briefs" in html
    assert "Opportunities" in html
    assert "exportCsv" in html


def _start_server(tmp_path: Path) -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _make_handler(tmp_path))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}"


def _make_handler(out_dir: Path):
    from painscout.dashboard import _load_report as load

    class H:
        pass

    import http.server

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            path = self.path.split("?")[0]
            if path == "/api/report":
                body = json.dumps(load(out_dir).to_dict()).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *args):  # noqa: A003
            pass

    return Handler


def test_dashboard_api_endpoint(report_dir: Path):
    import urllib.request

    server, url = _start_server(report_dir)
    try:
        with urllib.request.urlopen(f"{url}/api/report") as resp:  # noqa: S310
            data = json.loads(resp.read())
        assert data["opportunities"][0]["theme"] == "Manual work"
        assert data["opportunities"][0]["buy_intent"] is True
    finally:
        server.shutdown()
