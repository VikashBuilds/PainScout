"""Hacker News source — Algolia search API (free, no auth)."""

from __future__ import annotations

from painscout.models import PainPoint
from painscout.sources import Source

API = "https://hn.algolia.com/api/v1/search"


class HackerNewsSource(Source):
    name = "hackernews"

    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        params = {
            "query": query,
            "tags": "(story,ask_hn)",
            "hitsPerPage": limit,
            "numericFilters": "points>5",
        }
        with self._client() as client:
            resp = client.get(API, params=params)
            resp.raise_for_status()
            return self._parse(resp.json())

    @staticmethod
    def _parse(data: dict) -> list[PainPoint]:
        """Pure parser — unit-testable without network."""
        points: list[PainPoint] = []
        for hit in data.get("hits", []):
            title = hit.get("title") or hit.get("story_title") or ""
            text = hit.get("story_text") or ""
            if not title and not text:
                continue
            url = f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            points.append(
                PainPoint(
                    source="hackernews",
                    title=title,
                    text=text[:2000],
                    url=url,
                    created_at=hit.get("created_at", ""),
                    meta={"points": hit.get("points"), "num_comments": hit.get("num_comments")},
                )
            )
        return points
