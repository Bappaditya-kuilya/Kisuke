"""Provider configuration.

Configuration is external: environment variables and explicit overrides. No API
keys, endpoints, or models are hardcoded in source. Secrets are read from the
environment only.

Default behavior is local (offline). Cloud providers require explicit
configuration (API key / base URL) before they become available.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass
class ProviderConfig:
    """Resolved AI provider configuration."""

    provider: str = "local"
    model: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    api_key: str | None = None
    base_url: str | None = None

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> ProviderConfig:
        """Build configuration from the environment.

        Recognized variables:

        - ``KISUKE_AI_PROVIDER``  – provider name (default ``local``)
        - ``KISUKE_AI_MODEL``     – model name
        - ``KISUKE_AI_TEMPERATURE`` – float temperature
        - ``KISUKE_AI_MAX_TOKENS``  – integer token cap
        - ``KISUKE_AI_API_KEY``   – generic API key
        - ``KISUKE_AI_BASE_URL``  – generic base URL
        - ``<PROVIDER>_API_KEY``  – provider-specific key (e.g. ``OPENAI_API_KEY``)

        Cloud providers are only usable when their key (or a generic key) is set.
        """
        env = env if env is not None else dict(os.environ)
        provider = env.get("KISUKE_AI_PROVIDER", "local").strip() or "local"

        api_key = env.get("KISUKE_AI_API_KEY")
        if api_key is None:
            for key, value in env.items():
                if key.endswith("_API_KEY") and value:
                    api_key = value
                    break
        if api_key is None:
            api_key = env.get(f"{provider.upper()}_API_KEY")
        base_url = env.get("KISUKE_AI_BASE_URL")

        temperature = 0.2
        if raw_temp := env.get("KISUKE_AI_TEMPERATURE"):
            try:
                temperature = float(raw_temp)
            except ValueError:
                temperature = 0.2

        max_tokens: int | None = None
        if raw_max := env.get("KISUKE_AI_MAX_TOKENS"):
            try:
                max_tokens = int(raw_max)
            except ValueError:
                max_tokens = None

        return cls(
            provider=provider,
            model=env.get("KISUKE_AI_MODEL") or None,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            base_url=base_url,
        )

    def with_overrides(self, **overrides: Any) -> ProviderConfig:
        """Return a copy with the given fields overridden."""
        data = {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_key": self.api_key,
            "base_url": self.base_url,
        }
        data.update({k: v for k, v in overrides.items() if k in data})
        return ProviderConfig(**data)  # type: ignore[arg-type]


# Default base URL for OpenAI-compatible providers. It is a configurable default,
# never a hardcoded secret; callers may override it via ProviderConfig.base_url.
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
