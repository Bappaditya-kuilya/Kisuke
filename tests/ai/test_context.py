"""Tests for context packaging (immutable, minimal, prioritized)."""

from __future__ import annotations

from kisuke.ai.context import AIContext, package_context
from tests.ai.conftest import make_resume_result


def test_package_priority_order() -> None:
    ctx = package_context(make_resume_result())
    rendered = ctx.render()
    # Priority order: project, task, decisions, knowledge, resources.
    assert rendered.index("Project:") < rendered.index("Current Task:")
    assert rendered.index("Current Task:") < rendered.index("Related Decisions:")
    assert rendered.index("Related Decisions:") < rendered.index("Relevant Knowledge:")
    assert rendered.index("Relevant Knowledge:") < rendered.index("Resources:")


def test_package_contains_content() -> None:
    ctx = package_context(make_resume_result())
    rendered = ctx.render()
    assert "Ship the integration" in rendered  # project description
    assert "Write the adapter" in rendered  # task description
    assert "Use provider X" in rendered  # decision
    assert "Details about X" in rendered  # knowledge content


def test_context_is_immutable() -> None:
    ctx = package_context(make_resume_result())
    with __import__("pytest").raises(Exception):
        ctx.project = "mutated"  # type: ignore[misc]


def test_context_to_dict() -> None:
    ctx = package_context(make_resume_result())
    data = ctx.to_dict()
    assert data["project"] is not None
    assert isinstance(data["decisions"], list)
    assert isinstance(data["raw"], dict)


def test_empty_context_is_frozen_and_renderable() -> None:
    ctx = AIContext(project=None, task=None)
    assert ctx.render() == ""
