"""Tests for provider configuration (external, env-driven)."""

from __future__ import annotations

from kisuke.ai.config import ProviderConfig


def test_default_is_local() -> None:
    cfg = ProviderConfig.from_env({})
    assert cfg.provider == "local"
    assert cfg.api_key is None
    assert cfg.base_url is None


def test_reads_generic_env() -> None:
    env = {
        "KISUKE_AI_PROVIDER": "openai",
        "KISUKE_AI_MODEL": "gpt-4o",
        "KISUKE_AI_TEMPERATURE": "0.7",
        "KISUKE_AI_MAX_TOKENS": "512",
        "KISUKE_AI_API_KEY": "sk-test",
        "KISUKE_AI_BASE_URL": "https://example.com/v1",
    }
    cfg = ProviderConfig.from_env(env)
    assert cfg.provider == "openai"
    assert cfg.model == "gpt-4o"
    assert cfg.temperature == 0.7
    assert cfg.max_tokens == 512
    assert cfg.api_key == "sk-test"
    assert cfg.base_url == "https://example.com/v1"


def test_provider_specific_key() -> None:
    env = {"OPENAI_API_KEY": "sk-openai"}
    cfg = ProviderConfig.from_env(env)
    assert cfg.provider == "local"
    assert cfg.api_key == "sk-openai"


def test_invalid_temperature_keeps_default() -> None:
    cfg = ProviderConfig.from_env({"KISUKE_AI_TEMPERATURE": "not-a-float"})
    assert cfg.temperature == 0.2


def test_with_overrides_copies() -> None:
    cfg = ProviderConfig.from_env({})
    overridden = cfg.with_overrides(provider="openai", api_key="k")
    assert overridden.provider == "openai"
    assert overridden.api_key == "k"
    # Original is unchanged (immutability of configuration intent).
    assert cfg.provider == "local"
    assert cfg.api_key is None
