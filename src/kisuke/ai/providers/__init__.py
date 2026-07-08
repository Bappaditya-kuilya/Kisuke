"""AI provider adapters."""

from __future__ import annotations

from kisuke.ai.providers.local import LocalProvider
from kisuke.ai.providers.openai_compatible import OpenAICompatibleProvider

__all__ = ["LocalProvider", "OpenAICompatibleProvider"]
