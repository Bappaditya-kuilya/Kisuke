"""Shared fixtures for CLI tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def cli_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the CLI at an isolated repo and data directory."""
    repo = tmp_path / "repo"
    data = tmp_path / "data"
    monkeypatch.setenv("KISUKE_REPO_DIR", str(repo))
    monkeypatch.setenv("KISUKE_DATA_DIR", str(data))
    monkeypatch.setenv("KISUKE_LOG_LEVEL", "WARNING")
    return repo


@pytest.fixture
def runner(cli_env: Path) -> Path:
    """Initialize the repository before each test that needs it."""
    from kisuke.cli.main import main

    assert main(["init"]) == 0
    return cli_env
