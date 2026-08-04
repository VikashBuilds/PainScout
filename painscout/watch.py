"""Competitor app watch list — scan reviews of many apps, not just one.

App Store reviews use a numeric app id (e.g. `310633997` for WhatsApp iOS);
Google Play reviews use an Android package name (e.g. `com.whatsapp`).
A watch list lets PainScout scan *many* competitor apps in one run:

  PAINSCOUT_WATCH_APPS="ios:310633997|WhatsApp, android:com.whatsapp"

Entries are comma-separated, each `platform:id` or `platform:id|Display Name`.
Bare ids keep the legacy behaviour (treated as iOS, matching the pre-existing
`--app-id` semantics).
"""

from __future__ import annotations

import os


def parse_watch_apps(raw: str | None = None) -> list[dict]:
    """Parse the watch list from a string or the PAINSCOUT_WATCH_APPS env var.

    Returns [{"platform": "ios"|"android", "id": str, "name": str}, ...].
    Bare ids default to ios (legacy `--app-id` behaviour).
    """
    source = (raw or "").strip()
    if not source:
        source = os.environ.get("PAINSCOUT_WATCH_APPS", "").strip()
    if not source:
        return []

    entries: list[dict] = []
    for part in source.split(","):
        part = part.strip()
        if not part:
            continue
        name = ""
        # Optional display name after '|', e.g. "ios:310633997|WhatsApp"
        if "|" in part:
            part, name = part.split("|", 1)
            part, name = part.strip(), name.strip()
        if "::" in part:  # platform::id::name — rare, but explicit
            bits = part.split("::")
            platform, ident = bits[0], bits[1]
            if not name and len(bits) > 2:
                name = bits[2]
        elif ":" in part:
            platform, ident = part.split(":", 1)
            ident = ident.strip()
        else:
            platform, ident = "ios", part
        platform = platform.strip().lower()
        ident = ident.strip()
        if not ident:
            continue
        if platform not in ("ios", "android"):
            platform = "ios"
        entries.append({"platform": platform, "id": ident, "name": name})
    return entries
