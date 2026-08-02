"""Source base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod

import httpx

from painscout.config import Settings
from painscout.models import PainPoint


class Source(ABC):
    """A public source of customer complaints."""

    name: str = "base"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @abstractmethod
    def fetch(self, query: str, limit: int) -> list[PainPoint]:
        """Return up to `limit` pain points matching `query`."""

    def _client(self) -> httpx.Client:
        return httpx.Client(
            timeout=self.settings.timeout_seconds,
            headers={"User-Agent": self.settings.reddit_user_agent},
            follow_redirects=True,
        )


def get_sources(settings: Settings, names: str | None = None) -> list[Source]:
    """Instantiate the requested sources (comma-separated names), default: all."""
    from painscout.sources.appstore import AppStoreSource
    from painscout.sources.hackernews import HackerNewsSource
    from painscout.sources.reddit import RedditSource
    from painscout.sources.stackexchange import StackExchangeSource

    registry: dict[str, type[Source]] = {
        "reddit": RedditSource,
        "hn": HackerNewsSource,
        "stackexchange": StackExchangeSource,
        "appstore": AppStoreSource,  # optional — Apple's RSS feed is flaky
    }
    if not names:
        return [cls(settings) for cls in registry.values()]
    out: list[Source] = []
    for n in names.split(","):
        n = n.strip().lower()
        if n in registry:
            out.append(registry[n](settings))
    return out
