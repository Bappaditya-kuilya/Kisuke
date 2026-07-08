"""OpenAI-compatible AI provider adapter.

Talks to any OpenAI-compatible HTTP API (OpenAI, OpenRouter, local servers such as
Ollama/LM Studio exposing the `/v1` surface) using only the standard library
(``urllib``), so no third-party dependency is required. The adapter is optional:
it is only constructed/configured when a cloud provider is selected, and core
functionality never depends on it.

The provider never writes files or owns data; it only forwards prompts and
returns completions. Failures raise :class:`AIError`, which the service turns
into graceful degradation.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from kisuke.ai.config import DEFAULT_OPENAI_BASE_URL, ProviderConfig
from kisuke.ai.interfaces import (
    AIError,
    AIProvider,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ModelInfo,
)


class OpenAICompatibleProvider(AIProvider):
    """Adapter for OpenAI-compatible chat/embedding APIs."""

    name = "openai"
    kind = "cloud"

    def __init__(
        self,
        config: ProviderConfig,
        name: str = "openai",
        timeout: float = 30.0,
    ) -> None:
        self.config = config
        self.name = name
        self.timeout = timeout
        self.base_url = config.base_url or DEFAULT_OPENAI_BASE_URL

    def is_available(self) -> bool:
        # Availability requires credentials; reachability is checked by health_check.
        return bool(self.config.api_key)

    def health_check(self) -> bool:
        try:
            data = self._request("GET", f"{self.base_url}/models")
        except AIError:
            return False
        return isinstance(data, dict) and "data" in data

    def list_models(self) -> list[ModelInfo]:
        try:
            data = self._request("GET", f"{self.base_url}/models")
        except AIError:
            return []
        if not isinstance(data, dict):
            return []
        models = data.get("data", [])
        return [
            ModelInfo(id=str(m["id"]), provider=self.name)
            for m in models
            if isinstance(m, dict) and "id" in m
        ]

    def chat(self, request: ChatRequest) -> ChatResponse:
        payload = {
            "model": request.model or self.config.model or "",
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "temperature": request.temperature or self.config.temperature,
        }
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        elif self.config.max_tokens is not None:
            payload["max_tokens"] = self.config.max_tokens

        data = self._request("POST", f"{self.base_url}/chat/completions", payload)
        text = self._extract_content(data)
        model = None
        if isinstance(data, dict):
            model = data.get("model")
        return ChatResponse(text=text, model=model, provider=self.name, raw=data)

    def embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        payload = {
            "model": request.model or self.config.model or "",
            "input": request.texts,
        }
        data = self._request("POST", f"{self.base_url}/embeddings", payload)
        vectors: list[list[float]] = []
        if isinstance(data, dict):
            for item in data.get("data", []):
                if isinstance(item, dict) and isinstance(item.get("embedding"), list):
                    vectors.append([float(x) for x in item["embedding"]])
        return EmbeddingResponse(vectors=vectors, model=request.model, provider=self.name)

    # ------------------------------------------------------------------
    # HTTP internals
    # ------------------------------------------------------------------
    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _request(self, method: str, url: str, body: Any | None = None) -> Any:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(
            url, data=data, headers=self._headers(), method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace") if exc.fp else ""
            raise AIError(
                f"{method} {url} failed: {exc.code} {detail}", provider=self.name
            ) from exc
        except urllib.error.URLError as exc:
            raise AIError(
                f"{method} {url} failed: {exc.reason}", provider=self.name
            ) from exc
        if not raw:
            return None
        try:
            return json.loads(raw)
        except ValueError as exc:
            raise AIError(f"invalid JSON from {url}", provider=self.name) from exc

    @staticmethod
    def _extract_content(data: Any) -> str:
        if not isinstance(data, dict):
            return ""
        choices = data.get("choices", [])
        if not choices or not isinstance(choices[0], dict):
            return ""
        message = choices[0].get("message", {})
        if isinstance(message, dict):
            return str(message.get("content", ""))
        return ""
