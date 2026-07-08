"""Tests for the AI provider interface and shared types."""

from __future__ import annotations

import pytest

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
)


def test_provider_is_abstract() -> None:
    with pytest.raises(TypeError):
        AIProvider()  # type: ignore[abstract]


def test_dataclasses_roundtrip() -> None:
    req = ChatRequest(
        messages=[ChatMessage("user", "hi")], model="m", temperature=0.5, max_tokens=10
    )
    assert req.messages[0].role == "user"
    resp = ChatResponse(text="ok", model="m", provider="local", raw={"a": 1})
    assert resp.text == "ok"
    emb = EmbeddingResponse(vectors=[[0.1, 0.2]], model="m", provider="local")
    assert emb.vectors == [[0.1, 0.2]]
    info = ModelInfo(id="x", provider="local")
    assert info.id == "x"


def test_optional_operations_raise_by_default() -> None:
    class Minimal(AIProvider):
        name = "minimal"

        def is_available(self) -> bool:
            return True

        def health_check(self) -> bool:
            return True

        def chat(self, request: ChatRequest) -> ChatResponse:
            return ChatResponse(text="x", provider=self.name)

        def list_models(self) -> list[ModelInfo]:
            return [ModelInfo("x", self.name)]

    minimal = Minimal()
    with pytest.raises(NotImplementedError):
        minimal.embeddings(EmbeddingRequest(texts=["a"]))
    with pytest.raises(NotImplementedError):
        minimal.rerank(RerankRequest(query="q", documents=["d"]))


def test_ai_error_carries_provider() -> None:
    err = AIError("boom", provider="openai")
    assert err.provider == "openai"
    assert "boom" in str(err)
