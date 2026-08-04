"""Data models for PainScout."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass
class PainPoint:
    """A single piece of customer frustration found on a public source."""

    source: str  # e.g. "reddit", "hackernews", "appstore"
    title: str
    text: str
    url: str
    created_at: str = field(default_factory=_now)
    meta: dict = field(default_factory=dict)  # rating, subreddit, comments, etc.

    @property
    def full_text(self) -> str:
        return f"{self.title}\n{self.text}".strip()


@dataclass
class Opportunity:
    """A clustered pain point with a suggested fix and monetization angle."""

    theme: str  # short label, e.g. "Billing confusion in SaaS tools"
    pain: str  # what customers are suffering
    evidence: list[str]  # quotes
    sources: list[str]
    url: str  # best link
    suggested_solution: str  # what an AI SaaS / WhatsApp automation could do
    monetization: str  # how to charge for it
    score: float = 0.0  # 0-100 opportunity score
    buy_intent: bool = False  # customers literally say they'd pay for a fix
    trend: str = ""  # new | rising | hot | stable | cooling | dormant (from history)
    appearances: int = 0  # how many scans this theme has appeared in (window)
    market: dict = field(default_factory=dict)  # CompetitionResult.to_dict()

    def to_dict(self) -> dict:
        out = {
            "theme": self.theme,
            "pain": self.pain,
            "evidence": self.evidence,
            "sources": self.sources,
            "url": self.url,
            "suggested_solution": self.suggested_solution,
            "monetization": self.monetization,
            "score": round(self.score, 1),
            "buy_intent": self.buy_intent,
        }
        if self.trend:
            out["trend"] = self.trend
        if self.appearances:
            out["appearances"] = self.appearances
        if self.market:
            out["market"] = self.market
        return out


@dataclass
class Report:
    """The full output of a scan."""

    query: str
    generated_at: str = field(default_factory=_now)
    pain_points: list[PainPoint] = field(default_factory=list)
    opportunities: list[Opportunity] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "generated_at": self.generated_at,
            "pain_points": [
                {
                    "source": p.source,
                    "title": p.title,
                    "text": p.text,
                    "url": p.url,
                    "created_at": p.created_at,
                    "meta": p.meta,
                }
                for p in self.pain_points
            ],
            "opportunities": [o.to_dict() for o in self.opportunities],
        }
