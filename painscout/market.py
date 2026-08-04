"""Market / competition sanity-check for an opportunity.

Before a pain point becomes a "launch-ready brief", PainScout checks whether
the space is already crowded by querying free public search endpoints
(GitHub repository search + Hacker News Algolia). The result is a lightweight
`CompetitionResult` attached to the opportunity:

  - existing / links: what already exists
  - hn_hits: how much public discussion exists
  - level: low | medium | high   (crowding estimate)

This runs per-opportunity and is intentionally cheap (1 GitHub call + 1 HN
call each, with small sleeps to respect unauthenticated rate limits). Failures
degrade gracefully to `level = "unknown"`.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

import httpx

GITHUB_SEARCH_REPOS = "https://api.github.com/search/repositories"
HN_ALGOLIA = "https://hn.algolia.com/api/v1/search"


@dataclass
class CompetitionResult:
    level: str = "unknown"  # low | medium | high | unknown
    existing: list[str] = field(default_factory=list)  # "name (★stars)" strings
    links: list[str] = field(default_factory=list)
    hn_hits: int = 0
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "existing": self.existing[:8],
            "links": self.links[:8],
            "hn_hits": self.hn_hits,
            "note": self.note,
        }


def _keywords(theme: str) -> str:
    """Derive a 2-3 word GitHub search query from a theme label."""
    words = re.sub(r"[^a-z0-9 ]", " ", theme.lower()).split()
    stop = {
        "wish", "way", "tool", "app", "bot", "really", "solving", "customer",
        "this", "that", "and", "for", "the", "with", "from", "into",
    }
    filtered = [w for w in words if w not in stop and len(w) > 3]
    if not filtered:
        filtered = [w for w in words if len(w) > 3] or ["problem"]
    return " ".join(filtered[:3])


def _github_search(query: str, client: httpx.Client, timeout_secs: float) -> list[dict]:
    """Search public GitHub repos matching keywords. Returns [{name, stars, url}]."""
    try:
        resp = client.get(
            GITHUB_SEARCH_REPOS,
            params={"q": query, "per_page": 6, "sort": "stars"},
            timeout=timeout_secs,
        )
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return [
            {
                "name": it.get("full_name", ""),
                "stars": it.get("stargazers_count") or 0,
                "url": it.get("html_url", ""),
            }
            for it in items
            if it.get("full_name")
        ]
    except (httpx.HTTPError, KeyError, ValueError):
        return []


def _hn_hits(query: str, client: httpx.Client, timeout_secs: float) -> int:
    """Return number of Hacker News items mentioning the topic."""
    try:
        resp = client.get(HN_ALGOLIA, params={"query": query, "tags": "story"}, timeout=timeout_secs)
        resp.raise_for_status()
        return int(resp.json().get("nbHits") or 0)
    except (httpx.HTTPError, KeyError, ValueError, TypeError):
        return 0


def check_market(theme: str, user_agent: str = "PainScout/0.1", timeout: float = 15.0,
                 sleep: float = 6.0, with_hn: bool = True) -> CompetitionResult:
    """Run a tiny market check for a theme and classify competitiveness."""
    query = _keywords(theme)
    existing: list[dict] = []
    hn_hits = 0
    with httpx.Client(headers={"User-Agent": user_agent}, follow_redirects=True) as client:
        existing = _github_search(query, client, timeout)
        time.sleep(sleep)  # stay under unauthenticated GitHub rate cap
        if with_hn:
            hn_hits = _hn_hits(query, client, timeout)
    return _classify(query, existing, hn_hits)


def _classify(query: str, existing: list[dict], hn_hits: int) -> CompetitionResult:
    big = [r for r in existing if r["stars"] >= 1000]
    names = [f"{r['name']} (★{r['stars']})" for r in existing]
    links = [r["url"] for r in existing]

    # Heuristic crowding: many starred repos + lots of chatter => crowded.
    if len(big) >= 3 or (len(existing) >= 5 and hn_hits >= 200):
        level = "high"
    elif big or len(existing) >= 3 or hn_hits >= 40:
        level = "medium"
    else:
        level = "low"

    note = (
        f"'{query}': {len(existing)} similar repo(s), {hn_hits} HN stories. "
        + ("Space looks crowded — differentiation needed." if level == "high" else "Room to differentiate.")
    )
    return CompetitionResult(
        level=level,
        existing=names,
        links=links,
        hn_hits=hn_hits,
        note=note,
    )
