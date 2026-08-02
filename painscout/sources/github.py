"""GitHub issues source — search the public issues API (no auth needed).

People literally file issues begging for features or reporting broken
workflows — high-signal pain points with built-in buy intent.
Rate limit: 10 req/min unauthenticated, so we stay small.
"""

from __future__ import annotations

import time

from painscout.models import PainPoint
from painscout.sources import Source

API = "https://api.github.com/search/issues"

# Repos with vocal users complaining about workflow/productivity pain.
TARGET_REPOS = [
    "n8n-io/n8n",
    "zapier/zapier-platform",
    "microsoft/PowerToys",
    "obsidianmd/obsidian-releases",
    "notion-clone/notion-clone",
    "openai/whisper",
]


class GitHubIssuesSource(Source):
    name = "github"

    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        per_repo = max(1, limit // len(TARGET_REPOS))
        points: list[PainPoint] = []
        for repo in TARGET_REPOS:
            if len(points) >= limit:
                break
            try:
                points.extend(self._search_repo(repo, query, per_repo))
                time.sleep(6.2)  # stay under the 10 req/min unauthenticated cap
            except Exception:  # noqa: BLE001
                continue
        return points[:limit]

    def _search_repo(self, repo: str, query: str, limit: int) -> list[PainPoint]:
        q = f"repo:{repo} {query} is:issue is:open"
        params = {"q": q, "sort": "reactions", "per_page": str(limit)}
        with self._client() as client:
            resp = client.get(API, params=params)
            resp.raise_for_status()
            return self._parse(resp.json(), repo)

    @staticmethod
    def _parse(data: dict, repo: str = "") -> list[PainPoint]:
        """Pure parser — unit-testable without network."""
        points: list[PainPoint] = []
        for item in data.get("items", []):
            title = item.get("title", "")
            body = item.get("body") or ""
            if not title:
                continue
            points.append(
                PainPoint(
                    source="github",
                    title=title,
                    text=body[:2000],
                    url=item.get("html_url", ""),
                    created_at=item.get("created_at", ""),
                    meta={
                        "repo": repo or item.get("repository_url", "").split("/repos/")[-1],
                        "comments": item.get("comments"),
                        "reactions": item.get("reactions", {}).get("+1", 0),
                    },
                )
            )
        return points
