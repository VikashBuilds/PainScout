"""Rotating query / niche bank.

Instead of scanning the same single query every night, PainScout can rotate
through a bank of verified niches. Each day it deterministically picks the
query for that day (based on the Julian day), so consecutive nights explore
different verticals and the warehouse accrues trend data across niches.

The bank is configurable via `PAINSCOUT_QUERY_BANK` (JSON array of strings) or
`PAINSCOUT_QUERY` (a single default). Rotating only happens when the CLI/CI
passes `--rotate` (so `-q` and interactive usage are unaffected).
"""

from __future__ import annotations

import json
import os
from datetime import date

DEFAULT_BANK = [
    "wish there was a way to automate",
    "i waste hours every week",
    "customer support is terrible",
    "why is this so confusing to use",
    "wish i did not have to do this manually",
    "this tool keeps crashing",
    "paying too much for this app",
    "difficult to onboard new employees with this",
    "i'd pay for a tool that",
    "frustrated with billing and hidden fees",
    "takes forever to find what i need",
    "i want this but it does not exist",
    "please finally fix the wait times",
    "scammed by online payments",
    "need a better way to schedule and no-shows",
]


def load_bank() -> list[str]:
    """Return the configured bank (JSON from env) or the default bank."""
    raw = os.environ.get("PAINSCOUT_QUERY_BANK", "").strip()
    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and parsed and all(isinstance(x, str) for x in parsed):
                return [x.strip() for x in parsed if x.strip()]
        except (json.JSONDecodeError, TypeError):
            pass  # fall through to default
    return list(DEFAULT_BANK)


def pick_query(index: int | None = None, day: date | None = None) -> tuple[str, int]:
    """Pick the query for a given day (or today) from the rotating bank.

    Returns (query, index). Deterministic: same day -> same query, so the
    nightly CI and a manual re-run agree.
    """
    bank = load_bank()
    day = day or date.today()
    idx = index if index is not None else day.toordinal() % len(bank)
    return bank[idx], idx
