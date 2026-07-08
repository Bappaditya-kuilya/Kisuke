"""Minimal YAML-subset frontmatter parser/serializer and Markdown split/join.

This module handles only the constrained YAML produced for Kisuke frontmatter:
flat mappings of scalars (str/int), lists of scalars, and null. It deliberately
avoids external YAML libraries to keep the Infrastructure layer dependency-free.
"""

from __future__ import annotations

from typing import Any

from kisuke.domain.ids import EntityId


def _quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _emit_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, EntityId):
        return _quote(str(value))
    return _quote(str(value))


def dumps_yaml(data: dict[str, Any]) -> str:
    """Serialize a flat mapping to YAML-subset text."""
    lines: list[str] = []
    for key, value in data.items():
        if value is None:
            lines.append(f"{key}:")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{key}:")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"- {_emit_scalar(item)}")
        else:
            lines.append(f"{key}: {_emit_scalar(value)}")
    return "\n".join(lines) + "\n"


def _parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw == "" or raw in ("null", "~"):
        return None
    if raw in ("true", "false"):
        return raw == "true"
    if len(raw) >= 2 and raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    if len(raw) >= 2 and raw.startswith('"') and raw.endswith('"'):
        inner = raw[1:-1]
        return inner.encode("utf-8").decode("unicode_escape")
    try:
        return int(raw)
    except ValueError:
        return raw


def loads_yaml(text: str) -> dict[str, Any]:
    """Parse YAML-subset text into a flat mapping."""
    data: dict[str, Any] = {}
    lines = text.splitlines()
    i = 0
    current_key: str | None = None
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        stripped = line.lstrip()
        if stripped.startswith("- "):
            if current_key is not None:
                data.setdefault(current_key, [])
                existing = data[current_key]
                assert isinstance(existing, list)
                existing.append(_parse_scalar(stripped[2:].strip()))
            i += 1
            continue
        if ":" in line:
            key, _, raw = line.partition(":")
            key = key.strip()
            raw = raw.strip()
            if raw == "":
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].lstrip().startswith("- "):
                    data[key] = []
                    current_key = key
                    i = j
                    continue
                data[key] = None
                current_key = None
                i += 1
                continue
            data[key] = _parse_scalar(raw)
            current_key = None
            i += 1
            continue
        i += 1
    return data


def split_markdown(text: str) -> tuple[str, str]:
    """Split Markdown into (frontmatter_text, body_text)."""
    if not text.lstrip().startswith("---"):
        raise ValueError("Markdown is missing a frontmatter block")
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("Frontmatter block is not terminated")
    fm_text = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :])
    return fm_text, body


def join_markdown(fm_text: str, body: str) -> str:
    """Combine frontmatter text and body into Markdown."""
    if body and not body.endswith("\n"):
        body = body + "\n"
    if body:
        return f"---\n{fm_text}---\n\n{body}"
    return f"---\n{fm_text}---\n"
