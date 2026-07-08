"""Shared fixtures for AI layer tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from kisuke.ai.config import ProviderConfig
from kisuke.ai.interfaces import AIProvider, ChatResponse, ModelInfo
from kisuke.ai.registry import ProviderRegistry
from kisuke.ai.service import AIService


def make_entity(title: str, **kwargs: Any) -> SimpleNamespace:
    return SimpleNamespace(title=title, id=title.lower().replace(" ", "-"), **kwargs)


def make_resume_result() -> SimpleNamespace:
    """A minimal resume-like object for context packaging tests.

    Only the attributes read by ``package_context`` are provided.
    """
    return SimpleNamespace(
        mission=make_entity("Mission Alpha"),
        project=make_entity("Project Beta", description="Ship the integration", priority="high"),
        next_action=make_entity("Task 1", description="Write the adapter", due_date="2026-01-01"),
        related_tasks=[make_entity("Task 1"), make_entity("Task 2")],
        knowledge=[make_entity("Knowledge X", summary="Key notes", content="Details about X")],
        decisions=[make_entity("Decision Y", decision="Use provider X", reason="Simpler")],
        meetings=[],
        resources=[make_entity("Resource Z", content="https://example.com/z")],
        people=[],
        reviews=[],
    )


class MockProvider(AIProvider):
    """Test double for an AI provider."""

    name = "mock"
    kind = "cloud"

    def __init__(self, available: bool = True, fail: bool = False) -> None:
        self._available = available
        self._fail = fail
        self.calls: list[Any] = []
        self.last_request: Any = None

    def is_available(self) -> bool:
        return self._available

    def health_check(self) -> bool:
        return self._available

    def chat(self, request: Any) -> ChatResponse:  # type: ignore[override]
        from kisuke.ai.interfaces import AIError

        if self._fail:
            raise AIError("provider exploded", provider=self.name)
        self.calls.append(request)
        self.last_request = request
        return ChatResponse(text='{"priority": "high"}', model="mock-1", provider=self.name)

    def list_models(self) -> list[ModelInfo]:
        return [ModelInfo(id="mock-1", provider=self.name)]


def make_registry(*providers: AIProvider) -> ProviderRegistry:
    registry = ProviderRegistry()
    for provider in providers:
        registry.register(provider)
    return registry


def make_service(providers: list[AIProvider], provider: str = "local") -> AIService:
    registry = make_registry(*providers)
    config = ProviderConfig(provider=provider)
    return AIService(registry, config)
