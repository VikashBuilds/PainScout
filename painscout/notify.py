"""Telegram notifier — send the report to a chat via a bot."""

from __future__ import annotations

from pathlib import Path

import httpx

from painscout.config import Settings


def _api(method: str, token: str) -> str:
    return f"https://api.telegram.org/bot{token}/{method}"


def send_text(text: str, settings: Settings, parse_mode: str = "Markdown") -> bool:
    """Send a message; splits into chunks under Telegram's 4096-char limit."""
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False
    ok = True
    for chunk in _chunks(text, 3800):
        payload = {
            "chat_id": settings.telegram_chat_id,
            "text": chunk,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(_api("sendMessage", settings.telegram_bot_token), json=payload)
            if resp.status_code != 200:
                ok = False
    return ok


def send_file(path: Path, caption: str, settings: Settings) -> bool:
    """Send a report file as a Telegram document."""
    if not settings.telegram_bot_token or not settings.telegram_chat_id or not path.exists():
        return False
    with httpx.Client(timeout=60.0) as client:
        files = {"document": (path.name, path.read_bytes())}
        data = {"chat_id": settings.telegram_chat_id, "caption": caption}
        resp = client.post(_api("sendDocument", settings.telegram_bot_token), data=data, files=files)
        return resp.status_code == 200


def _chunks(text: str, size: int) -> list[str]:
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    while text:
        cut = text[:size]
        idx = cut.rfind("\n\n")
        if idx < size // 2:
            idx = cut.rfind("\n")
        if idx < size // 4:
            idx = size
        parts.append(text[:idx].rstrip())
        text = text[idx:].lstrip()
    return parts
