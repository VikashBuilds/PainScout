"""Google Play reviews source — public storefront endpoint.

NOTE: the Play storefront blocks many datacenter/cloud IPs (returns 405/400).
From a residential IP this works without auth. We fail gracefully so the
scan continues with other sources.
"""

from __future__ import annotations

import html as html_mod
import re

import httpx

from painscout.models import PainPoint
from painscout.sources import Source

REVIEW_URL = "https://play.google.com/store/getreviews"
DEFAULT_PACKAGE = "com.whatsapp"


class GooglePlaySource(Source):
    name = "googleplay"

    def _android_packages(self) -> list[dict]:
        """Packages to scan: watch list (android entries) or the legacy single id."""
        from painscout.watch import parse_watch_apps

        watched = [w for w in parse_watch_apps() if w["platform"] == "android"]
        if watched:
            return watched
        return [{"platform": "android", "id": self.settings.appstore_app_id or DEFAULT_PACKAGE, "name": ""}]

    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        points: list[PainPoint] = []
        for app in self._android_packages():
            if len(points) >= limit:
                break
            package = app["id"]
            app_name = app.get("name") or ""
            params = {
                "reviewSortOrder": "NEWEST",
                "pageNum": "0",
                "id": package,
                "reviewType": "1",
                "xhr": "1",
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://play.google.com/store/apps/details?id={package}&hl=en_US",
            }
            try:
                with httpx.Client(timeout=self.settings.timeout_seconds, headers=headers, follow_redirects=True) as client:
                    resp = client.post(REVIEW_URL, data=params)
                    resp.raise_for_status()
                    batch = self._parse(resp.text)
                for p in batch:
                    p.meta = {**(p.meta or {}), "appId": package, "appName": app_name}
                points.extend(batch)
            except Exception:  # noqa: BLE001 — blocked/errored storefront shouldn't kill the scan
                continue
        return points[:limit]

    @staticmethod
    def _parse(raw: str) -> list[PainPoint]:
        """Parse the JSONP-ish response: a JS array literal of review blobs."""
        points: list[PainPoint] = []
        if not raw or raw.startswith("<") or "Error" in raw[:200]:
            return points  # blocked / error page
        try:
            # Response is like: )]}'  [["...json..."],["..."],null]
            m = re.search(r"\[.*\]", raw[raw.find("[") :], re.DOTALL)
            if not m:
                return points
            import json

            data = json.loads(m.group(0))
            for blob in data:
                if not isinstance(blob, list) or not blob:
                    continue
                entry = blob[0]
                if isinstance(entry, dict):
                    # Some responses parse the review object directly
                    points.append(_review_to_point(entry))
                elif isinstance(entry, str):
                    try:
                        review = json.loads(entry)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(review, dict):
                        points.append(_review_to_point(review))
        except (ValueError, json.JSONDecodeError, IndexError):
            return points
        return [p for p in points if p is not None]


def _review_to_point(review: dict) -> PainPoint | None:
    text = review.get("text", "") or review.get("snippet", {}).get("text", "")
    if not text:
        return None
    title = text.split("\n")[0][:120]
    try:
        rating = int(review.get("starRating", 0))
    except (TypeError, ValueError):
        rating = 0
    return PainPoint(
        source="googleplay",
        title=html_mod.unescape(title),
        text=html_mod.unescape(text)[:2000],
        url=review.get("url", "") or "",
        created_at=str(review.get("timestamp", {}).get("iso", "")),
        meta={"rating": rating, "appId": review.get("appId", "")},
    )
