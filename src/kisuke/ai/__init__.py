"""AI package for Kisuke.

Provider-independent AI abstraction. The Core never talks to a provider directly;
it goes through :class:`~kisuke.ai.service.AIService`. Every provider implements
the contract in :mod:`kisuke.ai.interfaces`, is registered in a
:class:`~kisuke.ai.registry.ProviderRegistry`, and is selected by configuration.

AI is optional: with no provider configured, the service degrades gracefully and
core functionality is unaffected. AI never owns data and never becomes the source
of truth.
"""

from __future__ import annotations

from kisuke.ai.config import ProviderConfig
from kisuke.ai.context import AIContext, package_context
from kisuke.ai.interfaces import (
    AIError,
    AIProvider,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ModelInfo,
    RerankRequest,
    RerankResponse,
)
from kisuke.ai.prompts import Prompt, PromptLibrary
from kisuke.ai.registry import ProviderRegistry
from kisuke.ai.service import AIService, ServiceResult
from kisuke.ai.validation import ValidationResult, validate_response


def builtin_providers(config: ProviderConfig) -> list[AIProvider]:
    """Return the built-in provider instances for a configuration."""
    from kisuke.ai.providers.local import LocalProvider
    from kisuke.ai.providers.openai_compatible import OpenAICompatibleProvider

    return [
        LocalProvider(config),
        OpenAICompatibleProvider(config),
    ]


def build_registry(config: ProviderConfig) -> ProviderRegistry:
    """Construct a registry and register the built-in providers."""
    registry = ProviderRegistry()
    for provider in builtin_providers(config):
        registry.register(provider)
    return registry


__all__ = [
    "AIContext",
    "AIError",
    "AIProvider",
    "AIService",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "EmbeddingRequest",
    "EmbeddingResponse",
    "ModelInfo",
    "Prompt",
    "PromptLibrary",
    "ProviderConfig",
    "ProviderRegistry",
    "RerankRequest",
    "RerankResponse",
    "ServiceResult",
    "ValidationResult",
    "builtin_providers",
    "build_registry",
    "package_context",
    "validate_response",
]
