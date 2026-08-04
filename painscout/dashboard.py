"""Web dashboard — zero-dependency searchable UI over PainScout reports.

Serves the latest scan results (and any generated briefs) on a local HTTP
server. No external deps: stdlib http.server + inline HTML/JS.

Endpoints:
  GET /                — the dashboard UI
  GET /api/report      — merged report JSON (pain points + opportunities)
  GET /api/export.csv  — opportunities as CSV
  GET /briefs/<slug>.md — a project brief
"""

from __future__ import annotations

import csv
import io
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from painscout.brief import ProjectBrief
from painscout.config import Settings
from painscout.models import Report

_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PainScout Dashboard</title>
<style>
:root{--bg:#0b0f1a;--card:#131a2b;--line:#1e2a45;--acc:#6c5ce7;--acc2:#00cec9;--txt:#e8ecf4;--mut:#9aa5b8;--good:#2ecc71;--bad:#e74c3c}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--txt);min-height:100vh}
header{padding:28px 24px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
header h1{font-size:1.5rem}header h1 span{color:var(--acc2)}
.meta{color:var(--mut);font-size:.85rem}
.controls{display:flex;gap:10px;padding:18px 24px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
input,select,button{background:var(--card);border:1px solid var(--line);color:var(--txt);padding:9px 14px;border-radius:10px;font-size:.9rem}
input[type=text]{flex:1;min-width:220px}
button{cursor:pointer;border-color:var(--acc)}
button:hover{border-color:var(--acc2)}
main{max-width:1100px;margin:0 auto;padding:24px}
.opp{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-bottom:14px}
.opp-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}
.opp h2{font-size:1.15rem;margin-bottom:6px}
.score{font-size:1.4rem;font-weight:800;color:var(--acc2)}
.pain{color:var(--mut);margin:8px 0}
.sol{background:rgba(0,206,201,.07);border-left:3px solid var(--acc2);padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0}
.mono{color:var(--acc2);font-weight:600}
.buy{display:inline-block;background:rgba(46,204,113,.12);color:var(--good);border:1px solid rgba(46,204,113,.35);padding:3px 10px;border-radius:999px;font-size:.75rem;font-weight:700;margin-left:8px;vertical-align:middle}
.src{display:inline-block;background:rgba(108,92,231,.12);color:#b3a8ff;border-radius:999px;padding:3px 10px;font-size:.75rem;margin-right:6px}
.ev{margin-top:10px;font-size:.85rem;color:var(--mut)}
.ev li{margin-left:20px;margin-top:4px}
a{color:var(--acc2)}
.trend{display:inline-block;background:rgba(255,165,0,.12);color:#ffb347;border:1px solid rgba(255,165,0,.4);padding:3px 10px;border-radius:999px;font-size:.75rem;font-weight:700;margin-left:8px;vertical-align:middle}
.mk{display:inline-block;background:rgba(231,76,60,.1);color:#ff8a80;border:1px solid rgba(231,76,60,.35);padding:2px 8px;border-radius:999px;font-size:.7rem;margin-left:6px}
.mk.low{background:rgba(46,204,113,.1);color:var(--good);border-color:rgba(46,204,113,.35)}
.mk.medium{background:rgba(255,165,0,.1);color:#ffb347;border-color:rgba(255,165,0,.35)}
.tbl{width:100%;border-collapse:collapse;font-size:.85rem;margin:10px 0 24px}
.tbl th,.tbl td{border:1px solid var(--line);padding:8px 10px;text-align:left}
.tbl th{color:var(--mut);font-weight:600}
.hist{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-bottom:20px}
.brief{display:inline-block;margin-top:10px;font-size:.85rem;border:1px solid var(--line);padding:6px 12px;border-radius:8px;text-decoration:none}
.empty{text-align:center;color:var(--mut);padding:60px 0}
footer{padding:24px;text-align:center;color:var(--mut);font-size:.8rem}
</style>
</head>
<body>
<header>
  <h1>🔍 PainScout <span>Dashboard</span></h1>
  <div class="meta" id="meta">loading…</div>
</header>
<div class="controls">
  <input type="text" id="q" placeholder="Search pain points, themes, solutions…">
  <select id="src"><option value="">All sources</option></select>
  <select id="buy"><option value="">Buy intent: all</option><option value="1">💰 Only buy-intent</option></select>
  <select id="sort"><option value="score">Sort: score</option><option value="pain">Sort: pain (asc)</option><option value="evidence">Sort: evidence count</option></select>
  <button onclick="applyFilters()">Filter</button>
  <button onclick="exportCsv()">⬇ CSV</button>
  <button onclick="exportTrendsCsv()">📈 Trends CSV</button>
</div>
<div class="hist" id="hist"></div>
<main id="list"></main>
<footer>PainScout — complaints → validated, launch-ready AI products</footer>
<script>
let data = {opportunities: [], pain_points: []};
async function load() {
  const r = await fetch('/api/report');
  data = await r.json();
  const rh = await fetch('/api/history');
  if (rh.ok) { const h = await rh.json(); window.__hist = h; renderHistory(h); }
  const srcs = [...new Set(data.pain_points.map(p => p.source))].sort();
  const sel = document.getElementById('src');
  srcs.forEach(s => { const o = document.createElement('option'); o.value = s; o.textContent = s; sel.appendChild(o); });
  document.getElementById('meta').textContent =
    `${data.opportunities.length} opportunities · ${data.pain_points.length} pain points · ${new Date(data.generated_at || Date.now()).toLocaleString()}`;
  applyFilters();
}
function applyFilters() {
  const q = document.getElementById('q').value.toLowerCase();
  const src = document.getElementById('src').value;
  const buyOnly = document.getElementById('buy').value === '1';
  const sort = document.getElementById('sort').value;
  const srcCounts = {};
  data.pain_points.forEach(p => srcCounts[p.source] = (srcCounts[p.source]||0)+1);
  let opps = data.opportunities.filter(o => {
    if (src && !o.sources.includes(src)) return false;
    if (buyOnly && !o.buy_intent) return false;
    if (q) {
      const hay = (o.theme + ' ' + o.pain + ' ' + o.suggested_solution + ' ' + o.evidence.join(' ')).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
  if (sort === 'pain') opps.sort((a,b) => a.pain.length - b.pain.length);
  else if (sort === 'evidence') opps.sort((a,b) => b.evidence.length - a.evidence.length);
  else opps.sort((a,b) => b.score - a.score);
  const list = document.getElementById('list');
  if (!opps.length) { list.innerHTML = '<div class="empty">No opportunities match your filters 🕵️</div>'; return; }
  list.innerHTML = opps.map(o => `
    <div class="opp">
      <div class="opp-top">
        <div>
          <h2>${o.buy_intent ? '<span class="buy">💰 BUY INTENT</span>' : ''} ${esc(o.theme)}${o.trend ? '<span class="trend">🔺 '+esc(o.trend)+'</span>' : ''}${o.market&&o.market.level ? '<span class="mk '+esc(o.market.level)+'">🕵️ '+esc(o.market.level)+'</span>' : ''}</h2>
          <div>${o.sources.map(s => `<span class="src">${esc(s)} · ${srcCounts[s]||0}</span>`).join('')}</div>
        </div>
        <div class="score">${o.score}</div>
      </div>
      <p class="pain">${esc(o.pain)}</p>
      <div class="sol"><span class="mono">💡 Build:</span> ${esc(o.suggested_solution)}</div>
      <div><span class="mono">💳</span> ${esc(o.monetization)}</div>
      <ul class="ev">${o.evidence.slice(0,3).map(e => `<li>“${esc(e)}”</li>`).join('')}</ul>
      ${o.url ? `<a href="${esc(o.url)}" target="_blank">evidence link ↗</a>` : ''}
      <a class="brief" href="/briefs/?theme=${encodeURIComponent(o.theme)}" target="_blank">📄 view project brief</a>
    </div>`).join('');
}
function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function exportCsv() {
  const rows = [['theme','score','buy_intent','sources','pain','suggested_solution','monetization','url']];
  data.opportunities.forEach(o => rows.push([o.theme, o.score, o.buy_intent, o.sources.join('|'), o.pain.replace(/\\n/g,' '), o.suggested_solution.replace(/\\n/g,' '), o.monetization.replace(/\\n/g,' '), o.url]));
  const csv = rows.map(r => r.map(c => '"' + String(c).replace(/"/g,'""') + '"').join(',')).join('\\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], {type:'text/csv'}));
  a.download = 'painscout-opportunities.csv';
  a.click();
}
function renderHistory(h) {
  const el = document.getElementById('hist');
  if (!h || !h.themes || !h.themes.length) { el.innerHTML = ''; return; }
  const rows = h.themes.map(t =>
    `<tr><td>${esc(t.theme)}</td><td>${esc(t.trend)}</td><td>${t.occurrences}</td><td>${t.scans}</td><td>${t.avg_score}</td></tr>`).join('');
  el.innerHTML = `<h2 style="margin:0 0 6px">📈 30-day theme trends</h2>
    <table class="tbl"><thead><tr><th>Theme</th><th>Trend</th><th>Appearances</th><th>Scans</th><th>Avg score</th></tr></thead><tbody>${rows}</tbody></table>`;
}
function exportTrendsCsv() {
  if (!window.__hist || !window.__hist.themes) return;
  const rows = [['theme','trend','occurrences','scans','avg_score','first_seen','last_seen','last7','prev7']];
  window.__hist.themes.forEach(t => rows.push([t.theme, t.trend, t.occurrences, t.scans, t.avg_score, t.first_seen, t.last_seen, t.last7, t.prev7]));
  const csv = rows.map(r => r.map(c => '"' + String(c).replace(/"/g,'""') + '"').join(',')).join('\\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], {type:'text/csv'}));
  a.download = 'painscout-trends.csv';
  a.click();
}
load();
</script>
</body>
</html>
"""


def _load_report(out_dir: Path) -> Report:
    latest = out_dir / "latest.json"
    if latest.exists():
        data = json.loads(latest.read_text(encoding="utf-8"))
        return Report(
            query=data.get("query", ""),
            generated_at=data.get("generated_at", ""),
            pain_points=[_pp(p) for p in data.get("pain_points", [])],
            opportunities=[_opp(o) for o in data.get("opportunities", [])],
        )
    return Report(query="")


def _pp(d: dict):
    from painscout.models import PainPoint

    return PainPoint(
        source=d.get("source", ""),
        title=d.get("title", ""),
        text=d.get("text", ""),
        url=d.get("url", ""),
        created_at=d.get("created_at", ""),
        meta=d.get("meta", {}),
    )


def _opp(d: dict):
    from painscout.models import Opportunity

    return Opportunity(
        theme=d.get("theme", ""),
        pain=d.get("pain", ""),
        evidence=d.get("evidence", []),
        sources=d.get("sources", []),
        url=d.get("url", ""),
        suggested_solution=d.get("suggested_solution", ""),
        monetization=d.get("monetization", ""),
        score=d.get("score", 0),
        buy_intent=d.get("buy_intent", False),
    )


def _briefs_index(out_dir: Path) -> dict[str, ProjectBrief]:
    briefs_dir = out_dir / "briefs"
    out: dict[str, ProjectBrief] = {}
    if not briefs_dir.is_dir():
        return out
    for jf in sorted(briefs_dir.glob("*.json")):
        try:
            d = json.loads(jf.read_text(encoding="utf-8"))
            out[d.get("name", jf.stem)] = ProjectBrief(
                opportunity_theme=d.get("opportunity_theme", ""),
                name=d.get("name", jf.stem),
                tagline=d.get("tagline", ""),
                problem=d.get("problem", ""),
                solution=d.get("solution", ""),
                features=d.get("features", []),
                mvp_scope=d.get("mvp_scope", ""),
                tech_stack=d.get("tech_stack", []),
                build_estimate_days=d.get("build_estimate_days", 14),
                competitors=d.get("competitors", []),
                landing_copy=d.get("landing_copy", {}),
                whatsapp_bot=d.get("whatsapp_bot", {}),
                pricing_model=d.get("pricing_model", ""),
            )
        except (json.JSONDecodeError, KeyError):
            continue
    return out


def serve(out_dir: Path, port: int = 8791, open_browser: bool = True) -> None:
    from painscout.brief import render_brief_markdown

    briefs = _briefs_index(out_dir)

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            path = self.path.split("?")[0]
            if path == "/":
                self._send(200, _PAGE.encode(), "text/html; charset=utf-8")
            elif path == "/api/report":
                report = _load_report(out_dir)
                self._send(200, json.dumps(report.to_dict(), ensure_ascii=False).encode(), "application/json")
            elif path == "/api/history":
                hf = out_dir / "history.json"
                body = hf.read_text(encoding="utf-8") if hf.exists() else "{}"
                self._send(200, body.encode(), "application/json")
            elif path == "/api/trends.csv":
                cf = out_dir / "trends.csv"
                if cf.exists():
                    self._send(200, cf.read_bytes(), "text/csv")
                else:
                    self._send(404, b"no trends yet", "text/plain")
            elif path == "/api/export.csv":
                report = _load_report(out_dir)
                buf = io.StringIO()
                w = csv.writer(buf)
                w.writerow(["theme", "score", "buy_intent", "sources", "pain", "suggested_solution", "monetization", "url"])
                for o in report.opportunities:
                    w.writerow(
                        [o.theme, o.score, o.buy_intent, "|".join(o.sources), o.pain, o.suggested_solution, o.monetization, o.url]
                    )
                self._send(200, buf.getvalue().encode(), "text/csv")
            elif path == "/briefs/":
                if not briefs:
                    self._send(200, b"<h2>No briefs yet - run `painscout --brief` after a scan.</h2>", "text/html; charset=utf-8")
                    return
                items = "".join(
                    f'<li><a href="/briefs/{b.slug}.md">{b.name}</a> — {b.tagline}</li>'
                    for b in sorted(briefs.values(), key=lambda x: x.build_estimate_days)
                )
                self._send(200, f"<h2>Project briefs</h2><ul>{items}</ul>".encode(), "text/html; charset=utf-8")
            elif path.startswith("/briefs/"):
                slug = path.removeprefix("/briefs/").removesuffix(".md")
                for b in briefs.values():
                    if b.slug == slug:
                        self._send(200, render_brief_markdown(b).encode(), "text/markdown; charset=utf-8")
                        return
                self._send(404, b"brief not found", "text/plain")
            else:
                self._send(404, b"not found", "text/plain")

        def log_message(self, fmt: str, *args) -> None:  # noqa: A003
            print(f"  [dashboard] {fmt % args}")

    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    url = f"http://localhost:{port}"
    print(f"📊 PainScout dashboard: {url}")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:  # noqa: BLE001
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")


def serve_main(settings: Settings, port: int = 8791) -> None:
    serve(settings.out_dir, port=port)
