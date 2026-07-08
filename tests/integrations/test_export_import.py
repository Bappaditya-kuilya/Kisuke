"""Tests for the export interface and the Markdown import adapter.

Export is strictly read-only. Import is additive and safe: existing entity IDs
are skipped unless overwrite is explicitly requested, so canonical data is
never mutated unexpectedly.
"""

from __future__ import annotations

import json
from pathlib import Path

from kisuke.integrations import Exporter, MarkdownImporter
from tests.integrations.conftest import make_populated


def test_export_bundle(repo_root: Path, tmp_path: Path) -> None:
    ids = make_populated(repo_root)
    exporter = Exporter(repo_root)
    out = tmp_path / "bundle"
    result = exporter.export_bundle(out)
    assert result.count == 3
    assert (out / "task" / f"{ids[2]}.md").exists()
    assert (out / "mission" / f"{ids[0]}.md").exists()


def test_export_json(repo_root: Path, tmp_path: Path) -> None:
    make_populated(repo_root)
    exporter = Exporter(repo_root)
    out = tmp_path / "out.json"
    result = exporter.export_json(out)
    assert result.count == 3
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 3


def test_import_skips_existing(repo_root: Path, tmp_path: Path) -> None:
    ids = make_populated(repo_root)
    bundle = tmp_path / "bundle"
    Exporter(repo_root).export_bundle(bundle)
    importer = MarkdownImporter(repo_root)
    task_file = bundle / "task" / f"{ids[2]}.md"
    result = importer.import_file(task_file)
    assert result.skipped == [ids[2]]
    assert result.imported == []


def test_import_overwrite(repo_root: Path, tmp_path: Path) -> None:
    ids = make_populated(repo_root)
    bundle = tmp_path / "bundle"
    Exporter(repo_root).export_bundle(bundle)
    importer = MarkdownImporter(repo_root)
    task_file = bundle / "task" / f"{ids[2]}.md"
    result = importer.import_file(task_file, overwrite=True)
    assert result.imported == [ids[2]]


def test_import_directory_into_empty_repo(repo_root: Path, tmp_path: Path) -> None:
    make_populated(repo_root)
    bundle = tmp_path / "bundle"
    Exporter(repo_root).export_bundle(bundle)
    target = tmp_path / "target"
    importer = MarkdownImporter(target)
    result = importer.import_directory(bundle, recursive=True)
    assert len(result.imported) == 3
    assert (target / "tasks").exists()


def test_import_reports_errors(repo_root: Path, tmp_path: Path) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text("not a valid entity without frontmatter", encoding="utf-8")
    importer = MarkdownImporter(repo_root)
    result = importer.import_file(bad)
    assert result.errors
