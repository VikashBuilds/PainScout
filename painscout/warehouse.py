"""SQLite history warehouse — persistence, dedup and pain-trend scoring.

Every scan is appended to a SQLite database so that:
  - we can dedup duplicate pain points across scans,
  - we can measure which themes are *rising* over a rolling window,
  - the dashboard / report can surface a simple velocity signal.

The DB is kept outside the committed `reports/` tree (written under a
`/.history` dir). A lightweight `history.json` summary is written into
`reports/` so the static GitHub Pages dashboard can render trends without
needing the SQLite file.

This is intentionally dependency-light: stdlib `sqlite3` only.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from painscout.models import Report


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def dedup_points(points: list) -> tuple[list, int]:
    """Drop duplicate pain points within a single scan.

    Two pain points are "the same" if they share a non-empty normalized url,
    or (fallback) the same source + title. Returns (unique, dropped).
    """
    seen: set = set()
    unique: list = []
    dropped = 0
    for p in points:
        url = _norm(p, "url")
        key = url if url else f"{p.source}|{_norm(p, 'title')}".lower()
        if not key:
            key = re.sub(r"\s+", " ", _norm(p, "full_text"))[:200].lower()
        if key in seen:
            dropped += 1
            continue
        seen.add(key)
        unique.append(p)
    return unique, dropped


def _norm(obj, attr: str) -> str:
    try:
        v = getattr(obj, attr)
    except AttributeError:
        v = ""
    return (v or "").strip()


def _tostr(v) -> str:
    """Coerce a DB cell value to a safe string (some sources return lists/dicts)."""
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return " ".join(_tostr(x) for x in v)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


class Store:
    """SQLite-backed append-only history of scans + theme trends."""

    def __init__(self, db_path) -> None:
        self.db_path = Path(db_path) if not isinstance(db_path, Path) else db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self) -> None:
        c = self.conn
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL,
                query TEXT NOT NULL,
                mode TEXT DEFAULT 'ai',
                pain_count INTEGER DEFAULT 0,
                opp_count INTEGER DEFAULT 0
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS pain_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                title TEXT,
                text TEXT,
                url TEXT,
                created_at TEXT,
                meta_json TEXT,
                FOREIGN KEY(scan_id) REFERENCES scans(id)
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                theme TEXT NOT NULL,
                score REAL DEFAULT 0,
                sources_json TEXT,
                evidence_json TEXT,
                url TEXT,
                solution TEXT,
                monetization TEXT,
                buy_intent INTEGER DEFAULT 0,
                FOREIGN KEY(scan_id) REFERENCES scans(id)
            )
            """
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_opps_scan ON opportunities(scan_id, theme)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_pp_scan ON pain_points(scan_id, url)")
        c.commit()

    def record(self, report: Report, mode: str) -> int:
        """Persist one scan; returns the new scan id (pain points already deduped)."""
        c = self.conn
        cur = c.execute(
            "INSERT INTO scans(generated_at, query, mode, pain_count, opp_count) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                report.generated_at,
                report.query,
                mode,
                len(report.pain_points),
                len(report.opportunities),
            ),
        )
        scan_id = cur.lastrowid
        for p in report.pain_points:
            c.execute(
                "INSERT INTO pain_points(scan_id, source, title, text, url, created_at, meta_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    scan_id,
                    p.source,
                    _tostr(getattr(p, "title", None)),
                    _tostr(getattr(p, "text", None)),
                    _tostr(getattr(p, "url", None)) or "",
                    _tostr(getattr(p, "created_at", None)),
                    json.dumps(getattr(p, "meta", {}) or {}, ensure_ascii=False),
                ),
            )
        for o in report.opportunities:
            c.execute(
                "INSERT INTO opportunities(scan_id, theme, score, sources_json, evidence_json, "
                "url, solution, monetization, buy_intent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    scan_id,
                    o.theme,
                    o.score,
                    json.dumps(o.sources, ensure_ascii=False),
                    json.dumps(o.evidence, ensure_ascii=False),
                    o.url or "",
                    o.suggested_solution,
                    o.monetization,
                    int(bool(o.buy_intent)),
                ),
            )
        c.commit()
        return scan_id

    def latest_scan_id(self) -> int | None:
        r = self.conn.execute("SELECT MAX(id) AS m FROM scans").fetchone()
        return r["m"] if r and r["m"] is not None else None

    def close(self) -> None:
        self.conn.close()

    # ---- trends ----------------------------------------------------------

    def theme_trends(self, window_days: int = 30) -> dict[str, dict]:
        """Aggregate per-theme trends over the last `window_days`.

        Returns {theme: {occurrences, scans, first_seen, last_seen, avg_score,
        last7, prev7, recent}}.
        """
        cutoff = (datetime.now(UTC) - timedelta(days=window_days)).isoformat()
        cutoff_7 = (datetime.now(UTC) - timedelta(days=7)).isoformat()
        cutoff_14 = (datetime.now(UTC) - timedelta(days=14)).isoformat()

        rows = self.conn.execute(
            """
            SELECT o.scan_id, o.theme, o.score, o.evidence_json,
                   s.generated_at
            FROM opportunities o JOIN scans s ON s.id = o.scan_id
            WHERE s.generated_at >= ?
            """,
            (cutoff,),
        ).fetchall()

        trends: dict[str, dict] = {}
        for r in rows:
            t = trends.setdefault(
                r["theme"],
                {
                    "occurrences": 0,
                    "scans": set(),
                    "first_seen": r["generated_at"],
                    "last_seen": r["generated_at"],
                    "scores": [],
                    "evidence": set(),
                    "last7": 0,
                    "prev7": 0,
                    "under14": 0,
                },
            )
            t["occurrences"] += 1
            t["scans"].add(r["scan_id"])
            t["scores"].append(float(r["score"]))
            if r["generated_at"] < t["first_seen"]:
                t["first_seen"] = r["generated_at"]
            if r["generated_at"] > t["last_seen"]:
                t["last_seen"] = r["generated_at"]
            try:
                t["evidence"] |= set(json.loads(r["evidence_json"] or "[]"))
            except (json.JSONDecodeError, TypeError):
                pass
            if r["generated_at"] >= cutoff_7:
                t["last7"] += 1
            if cutoff_14 <= r["generated_at"] < cutoff_7:
                t["prev7"] += 1
            if r["generated_at"] >= cutoff_14:
                t["under14"] += 1

        out: dict[str, dict] = {}
        for theme, t in trends.items():
            avg = sum(t["scores"]) / len(t["scores"]) if t["scores"] else 0.0
            out[theme] = {
                "occurrences": t["occurrences"],
                "scans": len(t["scans"]),
                "first_seen": t["first_seen"],
                "last_seen": t["last_seen"],
                "avg_score": round(avg, 1),
                "last7": t["last7"],
                "prev7": t["prev7"],
                "recent": t["under14"] > 0,
            }
        return out

    @staticmethod
    def classify(trend: dict) -> str:
        """Label a theme trend for display."""
        if not trend.get("occurrences"):
            return "flat"
        if not trend.get("recent"):
            return "dormant"
        last7 = trend["last7"]
        prev7 = trend["prev7"]
        if trend["scans"] == 1:
            return "new"
        if last7 >= 2 and last7 > prev7:
            return "rising"
        if last7 > 0 and last7 >= prev7:
            return "hot"
        if last7 > 0:
            return "stable"
        return "cooling"

    def history_json(self) -> dict:
        """Compact summary for the committed dashboard history.json."""
        window = self.theme_trends()
        items = [
            {
                "theme": t,
                **{k: v for k, v in d.items() if k != "evidence"},
                "trend": Store.classify(d),
            }
            for t, d in window.items()
        ]
        items.sort(key=lambda x: (x.get("avg_score") or 0), reverse=True)
        return {
            "generated_at": _now_iso(),
            "window_days": 30,
            "theme_count": len(items),
            "themes": items,
        }


def default_db_path(out_dir: Path) -> Path:
    """History DB lives outside the committed reports tree (kept lean)."""
    return Path(out_dir) / ".history" / "painscout.db"


def write_history_artifacts(store: Store, out_dir: Path) -> tuple[Path, Path]:
    """Write reports/history.json + reports/trends.csv for the dashboard/export.

    The SQLite DB itself is intentionally NOT committed; these lightweight
    artifacts are, so the static dashboard and repo README can show trends.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    hist_json = out_dir / "history.json"
    hist_json.write_text(json.dumps(store.history_json(), indent=2, ensure_ascii=False), encoding="utf-8")

    trends_csv = out_dir / "trends.csv"
    data = store.history_json()
    header = ["theme", "trend", "occurrences", "scans", "avg_score", "first_seen", "last_seen", "last7", "prev7"]
    rows = [header]
    for t in data["themes"]:
        rows.append(
            [
                t["theme"],
                t.get("trend", ""),
                t.get("occurrences", 0),
                t.get("scans", 0),
                t.get("avg_score", 0),
                t.get("first_seen", ""),
                t.get("last_seen", ""),
                t.get("last7", 0),
                t.get("prev7", 0),
            ]
        )
    import csv
    import io

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    trends_csv.write_text(buf.getvalue(), encoding="utf-8")
    return hist_json, trends_csv
