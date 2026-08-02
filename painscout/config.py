"""Configuration — everything comes from environment variables with sane defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_QUERY = "wish there was a way to automate"
DEFAULT_APP_ID = "310633997"  # WhatsApp Messenger (lots of public complaints)


def _load_dotenv_files() -> None:
    """Load .env files if present (project dir, then ~/.hermes/.env)."""
    for p in (Path.cwd() / ".env", Path.home() / ".hermes" / ".env"):
        if p.is_file():
            try:
                from dotenv import dotenv_values

                for k, v in dotenv_values(p).items():
                    if v is not None:
                        os.environ.setdefault(k, v)
            except ImportError:
                # dotenv optional in some contexts; plain fallback parser
                for line in p.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


@dataclass
class Settings:
    query: str = DEFAULT_QUERY
    limit_per_source: int = 15
    timeout_seconds: float = 20.0

    # --- AI provider (OpenAI-compatible chat completions) ---
    # Priority: explicit PAINSCOUT_PROVIDER=zen|nim|openai, else NIM key, else zen key.
    zen_api_key: str = ""
    zen_base_url: str = "https://opencode.ai/zen/v1"
    zen_model: str = "deepseek-v4-flash-free"
    nim_api_key: str = ""
    nim_base_url: str = "https://integrate.api.nvidia.com/v1"
    nim_model: str = "nvidia/nemotron-3-ultra-550b-a55b"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    provider_override: str = ""

    # --- Telegram ---
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # --- Sources ---
    appstore_app_id: str = DEFAULT_APP_ID
    reddit_user_agent: str = "PainScout/0.1 (opportunity research bot)"

    # --- Output ---
    out_dir: Path = field(default_factory=lambda: Path("reports"))

    @property
    def ai_enabled(self) -> bool:
        return bool(self._provider_config()[0])

    def _provider_config(self) -> tuple[str, str, str]:
        """Return (api_key, base_url, model) for the active provider, or ("","","")."""
        p = (self.provider_override or "").strip().lower()
        if p == "zen":
            return self.zen_api_key, self.zen_base_url, self.zen_model
        if p == "nim":
            return self.nim_api_key, self.nim_base_url, self.nim_model
        if p == "openai":
            return self.openai_api_key, self.openai_base_url, self.openai_model
        if self.nim_api_key:
            return self.nim_api_key, self.nim_base_url, self.nim_model
        if self.zen_api_key:
            return self.zen_api_key, self.zen_base_url, self.zen_model
        if self.openai_api_key:
            return self.openai_api_key, self.openai_base_url, self.openai_model
        return "", "", ""

    @classmethod
    def from_env(cls, env: dict | None = None) -> Settings:
        _load_dotenv_files()
        e = os.environ if env is None else {k: str(v) for k, v in env.items()}

        def g(*names: str) -> str:
            for n in names:
                if e.get(n):
                    return e[n]
            return ""

        return cls(
            query=g("PAINSCOUT_QUERY") or DEFAULT_QUERY,
            limit_per_source=int(g("PAINSCOUT_LIMIT") or "15"),
            timeout_seconds=float(g("PAINSCOUT_TIMEOUT") or "20"),
            zen_api_key=g("OPENCODE_ZEN_API_KEY", "ZEN_API_KEY"),
            zen_base_url=g("OPENCODE_ZEN_BASE_URL") or "https://opencode.ai/zen/v1",
            zen_model=g("OPENCODE_ZEN_MODEL") or "deepseek-v4-flash-free",
            nim_api_key=g("NIM_API_KEY", "NVIDIA_API_KEY"),
            nim_base_url=g("NIM_BASE_URL") or "https://integrate.api.nvidia.com/v1",
            nim_model=g("NIM_MODEL") or "nvidia/nemotron-3-ultra-550b-a55b",
            openai_api_key=g("OPENAI_API_KEY"),
            openai_base_url=g("OPENAI_BASE_URL") or "https://api.openai.com/v1",
            openai_model=g("OPENAI_MODEL") or "gpt-4o-mini",
            provider_override=g("PAINSCOUT_PROVIDER"),
            telegram_bot_token=g("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=g("TELEGRAM_CHAT_ID", "TELEGRAM_HOME_CHANNEL"),
            appstore_app_id=g("PAINSCOUT_APP_ID") or DEFAULT_APP_ID,
            reddit_user_agent=g("PAINSCOUT_UA") or "PainScout/0.1 (opportunity research bot)",
            out_dir=Path(g("PAINSCOUT_OUT_DIR") or "reports"),
        )
