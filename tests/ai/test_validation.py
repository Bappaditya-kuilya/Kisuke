"""Tests for AI response validation."""

from __future__ import annotations

from kisuke.ai.validation import extract_json, validate_response


def test_empty_response_invalid() -> None:
    result = validate_response("   ")
    assert result.valid is False
    assert result.errors


def test_plain_text_valid() -> None:
    result = validate_response("a summary")
    assert result.valid is True
    assert result.data == "a summary"


def test_json_with_fence_extracted() -> None:
    text = 'Here you go:\n```json\n{"priority": "high"}\n```\n'
    data = extract_json(text)
    assert data == {"priority": "high"}


def test_expect_json_valid() -> None:
    result = validate_response(
        '{"priority": "high"}', expect_json=True, required_fields=("priority",)
    )
    assert result.valid is True
    assert result.data == {"priority": "high"}


def test_expect_json_missing_field() -> None:
    result = validate_response(
        '{"foo": 1}', expect_json=True, required_fields=("priority",)
    )
    assert result.valid is False
    assert "priority" in "; ".join(result.errors)


def test_expect_json_not_parseable() -> None:
    result = validate_response("not json", expect_json=True)
    assert result.valid is False
    assert result.errors
