"""App Store source — public iTunes customer reviews RSS feed (no auth)."""

from __future__ import annotations

from painscout.models import PainPoint
from painscout.sources import Source

REVIEW_FEED = "https://itunes.apple.com/us/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"


class AppStoreSource(Source):
    name = "appstore"

    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        """Fetch recent reviews; low-star reviews are the pain points.

        The feed returns ~10 reviews per page regardless of `limit`,
        so we pull pages until we have enough.
        """
        app_id = self.settings.appstore_app_id
        points: list[PainPoint] = []
        page = 1
        while len(points) < limit and page <= 5:
            url = REVIEW_FEED.format(page=page, app_id=app_id)
            with self._client() as client:
                resp = client.get(url)
                resp.raise_for_status()
                batch = self._parse(resp.json())
            if not batch:
                break
            points.extend(batch)
            page += 1
        return points[:limit]

    @staticmethod
    def _parse(data: dict) -> list[PainPoint]:
        """Pure parser — unit-testable without network."""
        points: list[PainPoint] = []
        entries = data.get("feed", {}).get("entry", [])
        if isinstance(entries, dict):  # single review comes back as a dict
            entries = [entries]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            title = _field(entry, "title")
            content = _field(entry, "content")
            rating = _field(entry, "im:rating")
            if not title and not content:
                continue
            # Skip stars as text ("1/5" -> 1)
            try:
                rating_int = int(str(rating).split("/")[0])
            except (ValueError, AttributeError):
                rating_int = 0
            url = _field(entry, "link") or ""
            if url.startswith("https://itunes.apple.com"):
                pass
            points.append(
                PainPoint(
                    source="appstore",
                    title=title,
                    text=content[:2000],
                    url=url,
                    created_at=_field(entry, "updated"),
                    meta={"rating": rating_int, "author": _field(entry, "author", "name")},
                )
            )
        return points


def _field(entry: dict, key: str, sub: str | None = None) -> str:
    """Pull a string field out of the messy iTunes JSON shape."""
    val = entry.get(key)
    if val is None:
        return ""
    if isinstance(val, dict):
        if sub and sub in val:
            val = val[sub]
        # Unwrap nested {"label": ...} wrappers (author -> name -> label).
        while isinstance(val, dict):
            val = val.get("label", "")
    return str(val).strip() if val is not None else ""
