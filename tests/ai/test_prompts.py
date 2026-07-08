"""Tests for the prompt abstraction (versioned, reusable, provider-independent)."""

from __future__ import annotations

import pytest

from kisuke.ai.prompts import Prompt, PromptLibrary


def test_builtin_prompts_registered() -> None:
    lib = PromptLibrary()
    for pid in ("system", "summarize", "explain", "next_action", "classify", "extract_keywords"):
        assert pid in lib.ids()


def test_render_substitutes_context() -> None:
    lib = PromptLibrary()
    rendered = lib.get("summarize").render(context="Project A\nTask 1")
    assert "Project A" in rendered
    assert "Context:" in rendered


def test_render_missing_field_raises() -> None:
    lib = PromptLibrary()
    with pytest.raises(KeyError):
        lib.get("explain").render(context="x")  # missing 'question'


def test_prompt_is_frozen() -> None:
    prompt = Prompt("custom", "1.0", "Hello {name}")
    with pytest.raises(AttributeError):
        prompt.template = "changed"  # type: ignore[misc]


def test_register_and_get_unknown() -> None:
    lib = PromptLibrary()
    lib.register(Prompt("custom", "1.0", "Hi {x}"))
    assert lib.get("custom").render(x="there") == "Hi there"
    with pytest.raises(KeyError):
        lib.get("does-not-exist")
