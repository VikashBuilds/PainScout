"""PainScout CLI — scan public sources for customer pain points."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from painscout import __version__
from painscout.analyzer import analyze
from painscout.config import Settings
from painscout.models import Report
from painscout.notify import send_file, send_text
from painscout.report import save_report
from painscout.sources import get_sources


def _make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="painscout",
        description="Find customer pain points and turn them into AI project ideas.",
    )
    p.add_argument("--version", action="version", version=f"painscout {__version__}")
    p.add_argument("-q", "--query", default=None, help="Search query (default from PAINSCOUT_QUERY)")
    p.add_argument("-s", "--sources", default=None, help="Comma-separated: reddit,hn,stackexchange,appstore (default: all)")
    p.add_argument("-l", "--limit", type=int, default=None, help="Max pain points per source")
    p.add_argument("-o", "--out-dir", default=None, help="Output directory (default: reports/)")
    p.add_argument("--no-ai", action="store_true", help="Force heuristic analyzer even if an API key exists")
    p.add_argument("--telegram", action="store_true", help="Send the report to Telegram")
    p.add_argument("--app-id", default=None, help="App Store app id for reviews (default: WhatsApp)")
    p.add_argument("--provider", choices=["zen", "nim", "openai"], default=None, help="Force AI provider")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _make_parser().parse_args(argv)
    settings = Settings.from_env()

    if args.query:
        settings.query = args.query
    if args.limit:
        settings.limit_per_source = args.limit
    if args.out_dir:
        settings.out_dir = Path(args.out_dir)
    if args.app_id:
        settings.appstore_app_id = args.app_id
    if args.provider:
        settings.provider_override = args.provider

    print(f"🔍 PainScout — scanning for: {settings.query!r}")
    sources = get_sources(settings, args.sources)
    if not sources:
        print("No valid sources selected. Use -s reddit,hn,appstore")
        return 2
    print(f"   Sources: {', '.join(s.name for s in sources)}")

    points: list = []
    for src in sources:
        try:
            found = src.fetch(settings.query, settings.limit_per_source)
            print(f"   [{src.name}] {len(found)} pain points")
            points.extend(found)
        except Exception as exc:  # noqa: BLE001 — source failure shouldn't kill the scan
            print(f"   [{src.name}] FAILED: {exc}")

    if not points:
        print("No pain points collected — check network/query.")
        return 1

    opportunities, used_mode = analyze(points, settings)
    if args.no_ai:
        used_mode = "fallback"
    print(f"   Analyzer: {'AI' if used_mode == 'ai' else 'heuristic fallback'} "
          f"-> {len(opportunities)} opportunities")

    report = Report(query=settings.query, pain_points=points, opportunities=opportunities)
    md_path, json_path = save_report(report, used_mode, settings.out_dir)
    print(f"✅ Report saved: {md_path}")
    print(f"   JSON: {json_path}")

    if args.telegram:
        summary = (
            f"📊 *PainScout Report*\n\n"
            f"Query: `{settings.query}`\n"
            f"Pain points scanned: {len(points)}\n"
            f"Opportunities: {len(opportunities)}\n\n"
            + "\n".join(
                f"{i}. *[{o.score:.0f}] {o.theme}*\n   {o.suggested_solution}"
                for i, o in enumerate(opportunities[:5], 1)
            )
        )
        send_text(summary, settings)
        send_file(md_path, f"PainScout report ({report.generated_at})", settings)
        print("📬 Sent to Telegram")
    return 0


if __name__ == "__main__":
    sys.exit(main())
