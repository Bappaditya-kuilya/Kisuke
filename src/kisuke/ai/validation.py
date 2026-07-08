"""Response validation.

AI responses are never trusted blindly. This module validates that a response is
non-empty and, when structured output is expected, that it parses as JSON and
carries the required fields. Validation never persists anything.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    """Outcome of validating an AI response."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    data: Any | None = None


_JSON_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def extract_json(text: str) -> dict[str, Any] | None:
    """Best-effort JSON extraction, tolerating markdown code fences."""
    if text is None:
        return None
    candidate = text.strip()
    fenced = _JSON_FENCE.search(candidate)
    if fenced is not None:
        candidate = fenced.group(1).strip()
    try:
        parsed = json.loads(candidate)
    except (ValueError, TypeError):
        return None
    return parsed if isinstance(parsed, dict) else None


def validate_response(
    text: str | None,
    *,
    required_fields: tuple[str, ...] = (),
    expect_json: bool = False,
) -> ValidationResult:
    """Validate a raw AI text response.

    - The response must be a non-empty string.
    - If ``expect_json`` is set, the response must parse as a JSON object.
    - Every name in ``required_fields`` must be present in that object.
    """
    if not text or not text.strip():
        return ValidationResult(valid=False, errors=["empty response"])

    if not expect_json:
        return ValidationResult(valid=True, data=text.strip())

    data = extract_json(text)
    if data is None:
        return ValidationResult(valid=False, errors=["response is not valid JSON"])

    missing = [field_name for field_name in required_fields if field_name not in data]
    if missing:
        return ValidationResult(
            valid=False, errors=[f"missing fields: {', '.join(missing)}"], data=data
        )

    return ValidationResult(valid=True, data=data)
