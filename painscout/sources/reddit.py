"""Reddit source — public search JSON endpoint (no auth for low-volume use)."""

from __future__ import annotations

import time

import httpx

from painscout.models import PainPoint
from painscout.sources import Source

SEARCH_URL = "https://www.reddit.com/search.json"
# Subreddits full of people complaining about business/tech problems.
TARGET_SUBREDDITS = [
    "SaaS",
    "Entrepreneur",
    "smallbusiness",
    "startups",
    "marketing",
    "ecommerce",
    "Productivity",
]


class RedditSource(Source):
    name = "reddit"

    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        per_sub = max(1, limit // len(TARGET_SUBREDDITS))
        points: list[PainPoint] = []
        for sub in TARGET_SUBREDDITS:
            if len(points) >= limit:
                break
            try:
                points.extend(self._search_subreddit(sub, query, per_sub))
                time.sleep(0.5)  # be polite to Reddit
            except (httpx.HTTPError, KeyError, ValueError):
                continue  # one subreddit failing shouldn't kill the scan
        return points[:limit]

    def _search_subreddit(self, subreddit: str, query: str, limit: int) -> list[PainPoint]:
        params = {
            "q": query,
            "restrict_sr": "1",
            "sort": "relevance",
            "limit": str(limit),
            "t": "year",
        }
        with self._client() as client:
            resp = client.get(f"{SEARCH_URL}?&subreddit={subreddit}", params=params)
            resp.raise_for_status()
            return self._parse(resp.json(), subreddit)

    @staticmethod
    def _parse(data: dict, subreddit: str = "") -> list[PainPoint]:
        """Pure parser — unit-testable without network."""
        points: list[PainPoint] = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            if post.get("stickied"):
                continue
            title = post.get("title", "")
            text = post.get("selftext", "") or ""
            if not title and not text:
                continue
            permalink = post.get("permalink", "")
            url = f"https://www.reddit.com{permalink}" if permalink else ""
            points.append(
                PainPoint(
                    source="reddit",
                    title=title,
                    text=text[:2000],
                    url=url,
                    created_at=post.get("created_utc", ""),
                    meta={
                        "subreddit": subreddit or post.get("subreddit"),
                        "score": post.get("score"),
                        "num_comments": post.get("num_comments"),
                    },
                )
            )
        return points
