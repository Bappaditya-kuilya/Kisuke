"""Tests for the repository scanner and incremental parser."""

from __future__ import annotations

from pathlib import Path

from kisuke.infrastructure.validation.parser import IncrementalParser
from kisuke.infrastructure.validation.scanner import RepositoryScanner
from kisuke.infrastructure.validation.validator import RepositoryValidator


def test_scanner_finds_all_entity_files(valid_repo: Path) -> None:
    paths = RepositoryScanner(valid_repo).discover()
    assert len(paths) == 11
    assert all(p.suffix == ".md" for p in paths)


def test_scanner_ignores_unknown_folders(valid_repo: Path) -> None:
    (valid_repo / "stray.txt").write_text("nope", encoding="utf-8")
    (valid_repo / "notes").mkdir()
    (valid_repo / "notes" / "x.md").write_text("nope", encoding="utf-8")
    paths = RepositoryScanner(valid_repo).discover()
    assert len(paths) == 11


def test_parser_reads_valid_entity(valid_repo: Path) -> None:
    path = next(iter(RepositoryScanner(valid_repo).discover()))
    result = IncrementalParser().parse_file(path)
    assert result.error is None
    assert result.entity is not None
    assert result.fm is not None


def test_parser_reports_unparseable_file(tmp_path: Path) -> None:
    bad = tmp_path / "missions"
    bad.mkdir()
    (bad / "x.md").write_text("this file has no frontmatter block", encoding="utf-8")
    result = IncrementalParser().parse_file(bad / "x.md")
    assert result.error is not None
    assert result.entity is None


def test_parser_reports_bad_owner(tmp_path: Path) -> None:
    folder = tmp_path / "missions"
    folder.mkdir()
    (folder / "x.md").write_text(
        "---\nid: '11111111-1111-1111-1111-111111111111'\n"
        "type: 'mission'\ntitle: 'M'\nowner: 'bogus'\nstatus: 'Active'\n"
        "tags:\nreferences:\nattachments:\n"
        "created_at: '2024-01-01T00:00:00+00:00'\n"
        "updated_at: '2024-01-01T00:00:00+00:00'\n---\n",
        encoding="utf-8",
    )
    result = IncrementalParser().parse_file(folder / "x.md")
    assert result.error is not None
    assert "PARSE_ERROR" not in result.error  # error is the raw construction message


def test_incremental_parser_avoids_reparse(valid_repo: Path) -> None:
    parser = IncrementalParser()
    validator = RepositoryValidator(valid_repo, parser=parser)
    validator.validate()
    first_count = parser.parse_count
    assert first_count == 11
    # Second pass: unchanged files are served from cache.
    validator.validate()
    assert parser.parse_count == first_count
