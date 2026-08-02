"""Stack Exchange source — free public API (no auth) across SO + sister sites.

People literally ask "how do I automate/fix X" here — pure pain signals.
"""

from __future__ import annotations

from painscout.models import PainPoint
from painscout.sources import Source

API = "https://api.stackexchange.com/2.3/search/advanced"
# Software Engineering, Workplace, Personal Productivity & Money are complaint goldmines.
SITES = ["stackoverflow", "softwareengineering", "workplace", "productivity", "money"]


class StackExchangeSource(Source):
    name = "stackexchange"

    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        per_site = max(1, limit // len(SITES))
        points: list[PainPoint] = []
        for site in SITES:
            if len(points) >= limit:
                break
            try:
                points.extend(self._search_site(site, query, per_site))
            except Exception:  # noqa: BLE001 — one site failing shouldn't kill the scan
                continue
        return points[:limit]

    def _search_site(self, site: str, query: str, limit: int) -> list[PainPoint]:
        params = {
            "order": "desc",
            "sort": "relevance",
            "q": query,
            "site": site,
            "pagesize": str(limit),
            "filter": "default",
        }
        with self._client() as client:
            resp = client.get(API, params=params)
            resp.raise_for_status()
            return self._parse(resp.json(), site)

    @staticmethod
    def _parse(data: dict, site: str = "") -> list[PainPoint]:
        """Pure parser — unit-testable without network."""
        points: list[PainPoint] = []
        for item in data.get("items", []):
            title = item.get("title", "")
            if not title:
                continue
            text = _html_to_text(item.get("body", "")) or item.get("tags", [])
            qid = item.get("question_id")
            url = f"https://{site or 'stackoverflow'}.com/q/{qid}" if qid else ""
            points.append(
                PainPoint(
                    source="stackexchange",
                    title=_html_to_text(title),
                    text=text[:2000],
                    url=url,
                    created_at=str(item.get("creation_date", "")),
                    meta={
                        "site": site,
                        "score": item.get("score"),
                        "answers": item.get("answer_count"),
                        "tags": item.get("tags", []),
                    },
                )
            )
        return points


def _html_to_text(s: str) -> str:
    """Crude HTML-to-text for question titles/bodies."""
    import html
    import re

    s = re.sub(r"<[^>]+>", "", s)  # remove tags entirely (no space artifacts)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace(" ?", "?").replace(" !", "!").replace(" ,", ",").replace(" .", ".")
