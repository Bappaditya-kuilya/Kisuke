"""Local (offline) AI provider adapter.

A dependency-free, deterministic provider that works with no network and no API
key. It is always available and is the default provider, satisfying the privacy
rule (Kisuke defaults to local). It performs simple, reproducible transformations
so the rest of the AI layer can be exercised end-to-end offline.

This adapter never contacts the network and never persists anything.
"""

from __future__ import annotations

import hashlib
import re

from kisuke.ai.config import ProviderConfig
from kisuke.ai.interfaces import (
    AIProvider,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ModelInfo,
)

_EMBED_DIM = 32
_TOKEN_RE = re.compile(r"[a-z0-9]+")


class LocalProvider(AIProvider):
    """Offline, deterministic AI provider."""

    name = "local"
    kind = "local"

    def __init__(self, config: ProviderConfig | None = None) -> None:
        self.config = config or ProviderConfig(provider="local")

    def is_available(self) -> bool:
        return True

    def health_check(self) -> bool:
        return True

    def list_models(self) -> list[ModelInfo]:
        return [ModelInfo(id="local", provider=self.name)]

    def chat(self, request: ChatRequest) -> ChatResponse:
        content = self._last_user_content(request)
        lowered = content.lower()

        if "classify" in lowered:
            return ChatResponse(
                text='{"priority": "medium"}', model="local", provider=self.name
            )
        if "extract keywords" in lowered:
            return ChatResponse(
                text='{"keywords": ["kisuke", "context", "task"]}',
                model="local",
                provider=self.name,
            )

        summary = self._extractive_summary(content)
        return ChatResponse(text=summary, model="local", provider=self.name)

    def embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        return EmbeddingResponse(
            vectors=[self._embed(text) for text in request.texts],
            model="local",
            provider=self.name,
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _last_user_content(request: ChatRequest) -> str:
        for message in reversed(request.messages):
            if message.role == "user":
                return message.content
        return request.messages[-1].content if request.messages else ""

    @staticmethod
    def _extractive_summary(content: str) -> str:
        context_block = ""
        if "Context:" in content:
            context_block = content.split("Context:", 1)[1]
        else:
            context_block = content
        lines = [line.strip() for line in context_block.splitlines() if line.strip()]
        head = lines[:3]
        preview = "\n".join(head) if head else content[:200]
        return f"[local summary]\n{preview}"

    @staticmethod
    def _embed(text: str) -> list[float]:
        vector = [0.0] * _EMBED_DIM
        tokens = _TOKEN_RE.findall(text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % _EMBED_DIM
            vector[index] += 1.0
        norm = sum(v * v for v in vector) ** 0.5
        if norm > 0.0:
            vector = [v / norm for v in vector]
        return vector
