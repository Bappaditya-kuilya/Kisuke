"""AI provider interface.

Every AI provider — local or cloud, OpenAI-compatible or not — implements the
same contract defined here. The Core and the :class:`~kisuke.ai.service.AIService`
never communicate with a provider directly; they go through this interface.

Design invariants (docs/engineering/10-ai-abstraction.md):

- AI is optional and stateless.
- Providers are interchangeable; the Core holds no provider-specific code.
- AI never owns data and never becomes the source of truth.
- Provider failures surface as :class:`AIError`; they must never break core flows.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class AIError(Exception):
    """Raised by a provider on operational failure (network, auth, parse)."""

    def __init__(self, message: str, *, provider: str | None = None) -> None:
        super().__init__(message)
        self.provider = provider


@dataclass
class ChatMessage:
    """A single chat turn."""

    role: str
    content: str


@dataclass
class ChatRequest:
    """A chat completion request."""

    messages: list[ChatMessage]
    model: str | None = None
    temperature: float = 0.0
    max_tokens: int | None = None


@dataclass
class ChatResponse:
    """A chat completion result."""

    text: str
    model: str | None = None
    provider: str | None = None
    raw: dict[str, Any] | None = None


@dataclass
class EmbeddingRequest:
    """A text-embedding request."""

    texts: list[str]
    model: str | None = None


@dataclass
class EmbeddingResponse:
    """A text-embedding result."""

    vectors: list[list[float]]
    model: str | None = None
    provider: str | None = None


@dataclass
class ModelInfo:
    """A model advertised by a provider."""

    id: str
    provider: str


@dataclass
class RerankRequest:
    """An optional reranking request."""

    query: str
    documents: list[str]
    model: str | None = None


@dataclass
class RerankResponse:
    """An optional reranking result (document indices, best first)."""

    ranked_indices: list[int]
    provider: str | None = None


class AIProvider(ABC):
    """Contract every Kisuke AI provider adapter implements."""

    name: str = ""
    kind: str = "generic"  # "local" or "cloud"

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the provider can be used in this environment."""

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the provider is reachable and operational."""

    @abstractmethod
    def chat(self, request: ChatRequest) -> ChatResponse:
        """Produce a chat completion."""

    @abstractmethod
    def list_models(self) -> list[ModelInfo]:
        """List models this provider can serve."""

    def embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Embed texts. Optional; raise NotImplementedError if unsupported."""
        raise NotImplementedError(f"{self.name} does not support embeddings")

    def rerank(self, request: RerankRequest) -> RerankResponse:
        """Rerank documents against a query. Optional."""
        raise NotImplementedError(f"{self.name} does not support reranking")
