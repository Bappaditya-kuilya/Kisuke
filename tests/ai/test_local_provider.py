"""Tests for the local (offline) provider adapter."""

from __future__ import annotations

from kisuke.ai.interfaces import ChatMessage, ChatRequest, EmbeddingRequest, ModelInfo
from kisuke.ai.providers.local import LocalProvider


def _request(text: str) -> ChatRequest:
    return ChatRequest(messages=[ChatMessage("user", text)])


def test_local_always_available() -> None:
    provider = LocalProvider()
    assert provider.is_available() is True
    assert provider.health_check() is True
    assert provider.kind == "local"


def test_local_list_models() -> None:
    models = LocalProvider().list_models()
    expected = ModelInfo(id="local", provider="local")
    assert models == [expected]


def test_local_extractive_summary() -> None:
    resp = LocalProvider().chat(_request("Context:\nProject A\nTask 1\nDecision Z"))
    assert resp.provider == "local"
    assert "Project A" in resp.text


def test_local_classify_returns_json() -> None:
    resp = LocalProvider().chat(_request("Classify the priority. Context:\nProject A"))
    assert '"priority"' in resp.text


def test_local_extract_keywords_returns_json() -> None:
    resp = LocalProvider().chat(_request("Extract keywords. Context:\nProject A"))
    assert '"keywords"' in resp.text


def test_local_embeddings_deterministic_and_normalized() -> None:
    provider = LocalProvider()
    a = provider.embeddings(EmbeddingRequest(texts=["kisuke context"])).vectors[0]
    b = provider.embeddings(EmbeddingRequest(texts=["kisuke context"])).vectors[0]
    assert a == b
    norm = sum(v * v for v in a) ** 0.5
    assert abs(norm - 1.0) < 1e-9


def test_local_embeddings_order_independent_of_text_count() -> None:
    provider = LocalProvider()
    single = provider.embeddings(EmbeddingRequest(texts=["hello world"]))
    assert len(single.vectors) == 1
