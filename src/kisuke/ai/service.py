"""AI service.

Orchestrates providers, prompts, context packaging, and response validation.
The service is the only AI entry point used by the rest of Kisuke; it never
imports a concrete provider. It is fully optional:

- If no provider is available, calls degrade gracefully (``ServiceResult.degraded``)
  instead of raising.
- Provider failures are caught and reported, never propagated to core workflows.
- The service never writes files, never mutates canonical data, and never persists
  AI responses automatically. AI responses are returned to the caller for explicit
  handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kisuke.ai.config import ProviderConfig
from kisuke.ai.context import AIContext
from kisuke.ai.interfaces import AIError, ChatMessage, ChatRequest
from kisuke.ai.prompts import PromptLibrary
from kisuke.ai.registry import ProviderRegistry
from kisuke.ai.validation import validate_response


@dataclass
class ServiceResult:
    """Outcome of an AI service call."""

    success: bool
    text: str = ""
    data: Any | None = None
    provider: str | None = None
    error: str | None = None
    degraded: bool = False


class AIService:
    """Provider-independent AI orchestration."""

    def __init__(
        self,
        registry: ProviderRegistry,
        config: ProviderConfig,
        prompts: PromptLibrary | None = None,
    ) -> None:
        self.registry = registry
        self.config = config
        self.prompts = prompts or PromptLibrary()

    def provider(self) -> Any:
        """Return the selected provider, or ``None`` if none available."""
        return self.registry.select(self.config.provider)

    def is_enabled(self) -> bool:
        """Whether a usable provider is currently available."""
        return self.provider() is not None

    def chat(
        self,
        prompt_id: str,
        context: AIContext,
        *,
        expect_json: bool = False,
        required_fields: tuple[str, ...] = (),
        question: str | None = None,
        temperature: float | None = None,
    ) -> ServiceResult:
        """Run a named prompt against the selected provider with packaged context."""
        provider = self.provider()
        if provider is None:
            return ServiceResult(
                success=False,
                error="no AI provider available",
                degraded=True,
            )

        try:
            prompt = self.prompts.get(prompt_id)
        except KeyError as exc:
            return ServiceResult(success=False, error=str(exc), degraded=True)

        try:
            user_text = prompt.render(context=context.render(), question=question or "")
        except KeyError as exc:
            return ServiceResult(
                success=False, error=f"prompt missing field: {exc}", degraded=True
            )

        messages = [
            ChatMessage("system", self.prompts.get("system").render()),
            ChatMessage("user", user_text),
        ]
        request = ChatRequest(
            messages=messages,
            model=self.config.model,
            temperature=temperature if temperature is not None else self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        try:
            response = provider.chat(request)
        except AIError as exc:
            return ServiceResult(
                success=False, error=str(exc), provider=provider.name, degraded=True
            )

        validation = validate_response(
            response.text, expect_json=expect_json, required_fields=required_fields
        )
        if not validation.valid:
            return ServiceResult(
                success=False,
                text=response.text,
                error="; ".join(validation.errors),
                provider=response.provider,
            )

        return ServiceResult(
            success=True,
            text=response.text,
            data=validation.data,
            provider=response.provider,
        )

    def list_models(self) -> list[str]:
        """List models across all available providers."""
        provider = self.provider()
        if provider is None:
            return []
        return [m.id for m in provider.list_models()]
