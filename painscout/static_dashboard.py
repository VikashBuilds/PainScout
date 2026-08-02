"""Static dashboard generator — a fully client-side HTML page for GitHub Pages.

Unlike `serve()` (a local HTTP server), this renders the same UI with pure
fetch() against JSON files committed to the repo, so it works on any static
host: GitHub Pages, Netlify, Vercel, S3…

Usage:
    painscout static [--out-dir reports] [--output docs/index.html]
"""

from __future__ import annotations

from pathlib import Path

from painscout.dashboard import _PAGE  # reuse the same UI shell

_STATIC_JS = """<script>
let data = {opportunities: [], pain_points: []};
let briefs = [];
async function load() {
  const [r1, r2] = await Promise.all([
    fetch('reports/latest.json').then(r => r.ok ? r.json() : null).catch(() => null),
    fetch('reports/briefs/index.json').then(r => r.ok ? r.json() : null).catch(() => null),
  ]);
  if (r1) data = r1;
  if (r2) briefs = r2;
  const srcs = [...new Set(data.pain_points.map(p => p.source))].sort();
  const sel = document.getElementById('src');
  srcs.forEach(s => { const o = document.createElement('option'); o.value = s; o.textContent = s; sel.appendChild(o); });
  document.getElementById('meta').textContent =
    (data.generated_at ? 'Last scan: ' + new Date(data.generated_at).toLocaleString() : 'No report yet') +
    ' · ' + data.opportunities.length + ' opportunities · ' + data.pain_points.length + ' pain points';
  renderBriefs();
  applyFilters();
}
function renderBriefs() {
  const el = document.getElementById('briefs');
  if (!briefs.length) { el.innerHTML = '<p class="empty">No briefs yet — run the nightly scan.</p>'; return; }
  el.innerHTML = briefs.map(b =>
    `<div class="opp"><h2>🚀 ${esc(b.name)}</h2>
     <p class="pain">${esc(b.tagline)}</p>
     <p class="mono">MVP ~${b.build_estimate_days} days · ${esc(b.pricing_model || '')}</p>
     <a class="brief" href="reports/briefs/${esc(b.slug)}.md" target="_blank">📄 brief (markdown)</a>
     <a class="brief" href="reports/landing/${esc(b.slug)}.html" target="_blank">🌐 landing page</a>
     <a class="brief" href="reports/briefs/${esc(b.slug)}.json" target="_blank">📦 JSON</a></div>`).join('');
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
          <h2>${o.buy_intent ? '<span class="buy">💰 BUY INTENT</span>' : ''} ${esc(o.theme)}</h2>
          <div>${o.sources.map(s => `<span class="src">${esc(s)} · ${srcCounts[s]||0}</span>`).join('')}</div>
        </div>
        <div class="score">${o.score}</div>
      </div>
      <p class="pain">${esc(o.pain)}</p>
      <div class="sol"><span class="mono">💡 Build:</span> ${esc(o.suggested_solution)}</div>
      <div><span class="mono">💳</span> ${esc(o.monetization)}</div>
      <ul class="ev">${o.evidence.slice(0,3).map(e => `<li>“${esc(e)}”</li>`).join('')}</ul>
      ${o.url ? `<a href="${esc(o.url)}" target="_blank">evidence link ↗</a>` : ''}
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
load();
</script>"""


def render_static_dashboard() -> str:
    """Full standalone HTML: same UI as the local server, data via fetch()."""
    # Swap the server-side script for the fetch-based one; add a briefs section.
    page = _PAGE
    start = page.find("<script>")
    end = page.find("</script>") + len("</script>")
    page = page[:start] + _STATIC_JS + page[end:]
    # Insert a briefs section between the controls and the list.
    anchor = '<main id="list"></main>'
    briefs_block = (
        '<h2 style="margin:28px 0 12px">🚀 Launch-ready project briefs</h2>'
        '<div id="briefs"></div>'
        '<h2 style="margin:28px 0 12px">🎯 Opportunities</h2>'
        f'{anchor}'
    )
    page = page.replace(anchor, briefs_block)
    return page


def save_static_dashboard(out_dir: Path, output: Path | None = None) -> Path:
    target = output or (Path("docs") / "index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_static_dashboard(), encoding="utf-8")
    return target
