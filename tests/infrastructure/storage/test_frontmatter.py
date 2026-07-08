"""Tests for the YAML-subset frontmatter parser/serializer and Markdown split/join."""

from __future__ import annotations

from kisuke.infrastructure.storage.frontmatter import (
    dumps_yaml,
    join_markdown,
    loads_yaml,
    split_markdown,
)


def test_dumps_scalar() -> None:
    assert dumps_yaml({"title": "Hello"}) == "title: 'Hello'\n"


def test_dumps_scalar_with_colon_quoted() -> None:
    assert dumps_yaml({"url": "http://x?a=1"}) == "url: 'http://x?a=1'\n"


def test_dumps_int_unquoted() -> None:
    assert dumps_yaml({"size": 2048}) == "size: 2048\n"


def test_dumps_bool() -> None:
    assert dumps_yaml({"flag": True}) == "flag: true\n"


def test_dumps_none() -> None:
    assert dumps_yaml({"summary": None}) == "summary:\n"


def test_dumps_empty_list() -> None:
    assert dumps_yaml({"tags": []}) == "tags:\n"


def test_dumps_list() -> None:
    text = dumps_yaml({"projects": ["a", "b"]})
    assert text == "projects:\n- 'a'\n- 'b'\n"


def test_roundtrip_scalar() -> None:
    data = {"title": "Hi", "size": 10, "flag": False, "note": None}
    assert loads_yaml(dumps_yaml(data)) == data


def test_roundtrip_list() -> None:
    data = {"tags": ["x", "y"]}
    assert loads_yaml(dumps_yaml(data)) == data


def test_empty_list_serializes_to_null_like_key() -> None:
    # Both empty list and null map to `key:` and parse back to None; the
    # serializer normalizes None -> [] for list fields.
    text = dumps_yaml({"tags": []})
    assert text == "tags:\n"
    assert loads_yaml(text) == {"tags": None}


def test_loads_parses_quoted_string() -> None:
    assert loads_yaml("title: 'a: b'") == {"title": "a: b"}


def test_loads_int_coercion() -> None:
    assert loads_yaml("size: 1024") == {"size": 1024}


def test_loads_non_numeric_string_stays_string() -> None:
    assert loads_yaml("value: 12abc") == {"value": "12abc"}


def test_dumps_scalar_with_quote_escaped() -> None:
    assert dumps_yaml({"note": "it's ok"}) == "note: 'it''s ok'\n"


def test_loads_double_quoted_unicode_escape() -> None:
    assert loads_yaml('note: "a\\nb"') == {"note": "a\nb"}


def test_loads_list_items() -> None:
    a = "11111111-1111-1111-1111-111111111111"
    b = "22222222-2222-2222-2222-222222222222"
    text = f"refs:\n- '{a}'\n- '{b}'\n"
    assert loads_yaml(text) == {
        "refs": [
            "11111111-1111-1111-1111-111111111111",
            "22222222-2222-2222-2222-222222222222",
        ]
    }


def test_split_markdown_basic() -> None:
    text = "---\nid: '1'\ntitle: 'x'\n---\n\n# Body\n\ntext\n"
    fm, body = split_markdown(text)
    assert fm == "id: '1'\ntitle: 'x'"
    assert body.strip() == "# Body\n\ntext"


def test_split_markdown_missing_block() -> None:
    import pytest

    with pytest.raises(ValueError):
        split_markdown("no frontmatter here")


def test_split_markdown_unterminated() -> None:
    import pytest

    with pytest.raises(ValueError):
        split_markdown("---\nid: '1'\n")


def test_join_markdown_with_body() -> None:
    result = join_markdown("id: '1'\n", "# Body\n\ntext\n")
    assert result == "---\nid: '1'\n---\n\n# Body\n\ntext\n"


def test_join_markdown_without_body() -> None:
    assert join_markdown("id: '1'\n", "") == "---\nid: '1'\n---\n"


def test_join_then_split_is_stable() -> None:
    fm = "id: '1'\ntitle: 'x'\n"
    body = "# Note\n\nhello\n"
    out = join_markdown(fm, body)
    back_fm, back_body = split_markdown(out)
    assert back_fm == fm.rstrip("\n")
    assert back_body.strip() == body.strip()
