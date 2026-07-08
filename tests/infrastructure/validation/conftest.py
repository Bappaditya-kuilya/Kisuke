"""Shared fixtures for Storage-layer validation tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from kisuke.domain.entities import EntityType
from kisuke.infrastructure.storage.frontmatter import dumps_yaml, join_markdown
from kisuke.infrastructure.storage.repository import FOLDER_NAMES
from tests.infrastructure.storage.conftest import make_all


def md_from_fm(fm: dict) -> str:
    return join_markdown(dumps_yaml(fm), "")


def write_fm(root: Path, et_value: str, filename: str, fm: dict) -> Path:
    folder = FOLDER_NAMES[EntityType(et_value)]
    path = Path(root) / folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md_from_fm(fm), encoding="utf-8")
    return path


@pytest.fixture
def valid_repo(tmp_path: Path) -> Path:
    from kisuke.infrastructure.storage.repository import FileRepository

    repo = FileRepository(tmp_path)
    for entity in make_all():
        repo.save(entity)
    return tmp_path


TS = "2024-01-01T00:00:00+00:00"
