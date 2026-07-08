"""Tests for the OpenAI-compatible provider adapter.

The HTTP layer (``urllib.request``) is mocked so no network is touched. These
tests verify request construction, response parsing, and graceful error handling.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from unittest import mock

from kisuke.ai.config import ProviderConfig
from kisuke.ai.interfaces import AIError, ChatMessage, ChatRequest, EmbeddingRequest
from kisuke.ai.providers.openai_compatible import OpenAICompatibleProvider


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._bytes = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def read(self) -> bytes:
        return self._bytes


def _provider(api_key: str = "sk-test") -> OpenAICompatibleProvider:
    return OpenAICompatibleProvider(
        ProviderConfig(provider="openai", api_key=api_key, model="gpt-4o")
    )


def test_not_available_without_key() -> None:
    provider = OpenAICompatibleProvider(ProviderConfig(provider="openai", api_key=None))
    assert provider.is_available() is False


def test_health_check_true() -> None:
    provider = _provider()
    with mock.patch(
        "urllib.request.urlopen", return_value=FakeResponse({"data": [{"id": "gpt-4o"}]})
    ):
        assert provider.health_check() is True


def test_health_check_false_on_error() -> None:
    provider = _provider()
    with mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("down"),
    ):
        assert provider.health_check() is False


def test_chat_builds_request_and_parses() -> None:
    provider = _provider()
    fake = FakeResponse({"choices": [{"message": {"content": "hello"}}], "model": "gpt-4o"})
    with mock.patch("urllib.request.urlopen", return_value=fake) as patched:
        resp = provider.chat(ChatRequest(messages=[ChatMessage("user", "hi")]))
    assert resp.text == "hello"
    assert resp.model == "gpt-4o"
    assert resp.provider == "openai"

    sent = json.loads(patched.call_args[0][0].data.decode("utf-8"))
    assert sent["model"] == "gpt-4o"
    assert sent["messages"][0]["content"] == "hi"
    assert "Authorization" in patched.call_args[0][0].headers


def test_list_models_parses() -> None:
    provider = _provider()
    with mock.patch(
        "urllib.request.urlopen",
        return_value=FakeResponse({"data": [{"id": "gpt-4o"}, {"id": "gpt-4o-mini"}]}),
    ):
        models = provider.list_models()
    assert {m.id for m in models} == {"gpt-4o", "gpt-4o-mini"}


def test_list_models_empty_on_error() -> None:
    provider = _provider()
    with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("x")):
        assert provider.list_models() == []


def test_embeddings_parses() -> None:
    provider = _provider()
    payload = {"data": [{"embedding": [0.1, 0.2]}, {"embedding": [0.3, 0.4]}]}
    with mock.patch("urllib.request.urlopen", return_value=FakeResponse(payload)):
        resp = provider.embeddings(EmbeddingRequest(texts=["a", "b"]))
    assert resp.vectors == [[0.1, 0.2], [0.3, 0.4]]


def test_http_error_raises_ai_error() -> None:
    provider = _provider()
    with mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("url", 401, "no", {}, None),
    ):
        try:
            provider.chat(ChatRequest(messages=[ChatMessage("user", "hi")]))
            raise AssertionError("expected AIError")
        except AIError as exc:
            assert exc.provider == "openai"
