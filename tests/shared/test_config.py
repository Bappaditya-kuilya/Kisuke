"""Tests for Kisuke configuration resolution."""

from __future__ import annotations

import logging
from pathlib import Path

from kisuke.shared.config import DEFAULT_DATA_DIR, Config


def test_default_config_uses_home_data_dir(monkeypatch) -> None:
    monkeypatch.delenv("KISUKE_DATA_DIR", raising=False)
    monkeypatch.delenv("KISUKE_LOG_LEVEL", raising=False)

    config = Config.from_env()

    assert config.data_dir == DEFAULT_DATA_DIR
    assert config.index_dir == DEFAULT_DATA_DIR / "index"
    assert config.cache_dir == DEFAULT_DATA_DIR / "cache"
    assert config.log_level == logging.INFO


def test_data_dir_override_from_env(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KISUKE_DATA_DIR", str(tmp_path / "data"))

    config = Config.from_env()

    assert config.data_dir == tmp_path / "data"
    assert config.index_dir == tmp_path / "data" / "index"


def test_log_level_parsed_from_env(monkeypatch) -> None:
    monkeypatch.setenv("KISUKE_LOG_LEVEL", "debug")

    config = Config.from_env()

    assert config.log_level == logging.DEBUG


def test_ensure_dirs_creates_paths(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KISUKE_DATA_DIR", str(tmp_path / "data"))

    config = Config.from_env()
    config.ensure_dirs()

    assert config.data_dir.is_dir()
    assert config.index_dir.is_dir()
    assert config.cache_dir.is_dir()
