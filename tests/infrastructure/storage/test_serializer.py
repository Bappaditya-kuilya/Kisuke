"""Tests for entity <-> Markdown serialization.

Covers lossless round-tripping, canonical frontmatter shape, golden-file
stability, references-stored-as-IDs, and UTF-8 handling.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kisuke.domain.entities import EntityType
from kisuke.infrastructure.storage.frontmatter import loads_yaml, split_markdown
from kisuke.infrastructure.storage.serializer import (
    entity_to_markdown,
    markdown_to_entity,
)

GOLDEN_DIR = Path(__file__).parent / "golden"

UNIVERSAL_CORE = ["id", "type", "title", "owner", "status"]
TAIL = ["tags", "references", "attachments", "created_at", "updated_at"]

SPECIFIC: dict[EntityType, list[str]] = {
    EntityType.MISSION: ["priority", "projects", "reviews"],
    EntityType.PROJECT: [
        "priority", "next_action", "tasks", "knowledge",
        "decisions", "meetings", "resources", "people",
    ],
    EntityType.TASK: ["priority", "due_date", "estimated_time"],
    EntityType.KNOWLEDGE: ["resources"],
    EntityType.COOKBOOK: ["category"],
    EntityType.DECISION: [],
    EntityType.MEETING: ["date", "people", "projects", "tasks", "decisions", "resources"],
    EntityType.PERSON: ["role", "organization", "email", "links"],
    EntityType.RESOURCE: ["resource_type", "url"],
    EntityType.REVIEW: [
        "review_type", "date", "completed_projects", "blocked_projects", "next_actions",
    ],
    EntityType.ATTACHMENT: ["filename", "mime_type", "size", "checksum"],
}

EXPECTED_FRONT: dict[EntityType, list[str]] = {
    et: UNIVERSAL_CORE + SPECIFIC[et] + TAIL for et in EntityType
}


def _front_keys(markdown: str) -> list[str]:
    fm_text, _ = split_markdown(markdown)
    return list(loads_yaml(fm_text).keys())


def test_roundtrip_lossless(entities: list) -> None:
    for entity in entities:
        restored = markdown_to_entity(entity_to_markdown(entity))
        assert restored == entity


def test_roundtrip_idempotent(entities: list) -> None:
    for entity in entities:
        once = entity_to_markdown(entity)
        twice = entity_to_markdown(markdown_to_entity(once))
        assert once == twice


def test_frontmatter_keys_match_canonical_schema(entity_by_type: dict) -> None:
    for et, entity in entity_by_type.items():
        assert _front_keys(entity_to_markdown(entity)) == EXPECTED_FRONT[et]


def test_required_universal_fields_present(entity_by_type: dict) -> None:
    for entity in entity_by_type.values():
        fm_text, _ = split_markdown(entity_to_markdown(entity))
        fm = loads_yaml(fm_text)
        for field in ("id", "type", "title", "owner", "status", "created_at", "updated_at"):
            assert field in fm


def test_references_stored_only_as_ids(entity_by_type: dict) -> None:
    project = entity_by_type[EntityType.PROJECT]
    fm_text, _ = split_markdown(entity_to_markdown(project))
    fm = loads_yaml(fm_text)
    # Every referenced value is a bare UUID string, never a nested mapping.
    for key in ("tasks", "knowledge", "decisions", "meetings", "resources", "people"):
        for value in fm[key]:
            assert isinstance(value, str)
            assert len(value) == 36  # UUID length, no nested objects


def test_utf8_roundtrip() -> None:
    from datetime import UTC, datetime

    from kisuke.domain.entities import Task
    from kisuke.domain.ids import EntityId
    from kisuke.domain.lifecycle import TaskStatus
    from kisuke.domain.owner import Owner
    from kisuke.domain.timestamp import Timestamp

    ts = Timestamp.from_datetime(datetime(2024, 1, 1, tzinfo=UTC))
    task = Task(
        id=EntityId.from_string("11111111-1111-1111-1111-111111111111"),
        title="日本語タイトル — café",
        owner=Owner.of(EntityId.from_string("22222222-2222-2222-2222-222222222222")),
        status=TaskStatus.TODO,
        description="Unicode: ünïçödé ✓ 日本語",
        created_at=ts,
        updated_at=ts,
    )
    text = entity_to_markdown(task)
    assert "日本語タイトル — café" in text
    assert "Unicode: ünïçödé ✓ 日本語" in text
    restored = markdown_to_entity(text)
    assert restored == task


def test_golden_files_match(entity_by_type: dict) -> None:
    for et, entity in entity_by_type.items():
        golden = GOLDEN_DIR / f"{et.value}.md"
        assert golden.exists(), f"missing golden file {golden}"
        expected = golden.read_text(encoding="utf-8")
        assert entity_to_markdown(entity) == expected


def test_load_expected_type_mismatch(entity_by_type: dict) -> None:

    text = entity_to_markdown(entity_by_type[EntityType.TASK])
    with pytest.raises(ValueError):
        markdown_to_entity(text, expected_type=EntityType.PROJECT)


def test_person_links_roundtrip(entity_by_type: dict) -> None:
    person = entity_by_type[EntityType.PERSON]
    restored = markdown_to_entity(entity_to_markdown(person))
    assert restored == person
    assert "https://example.com" in restored.links
