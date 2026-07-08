"""Snapshot tests.

Capture exact, deterministic CLI output for stable commands and compare against
stored snapshots. On first run (no snapshot file present) the snapshot is
written; subsequent runs verify against it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kisuke.cli.main import main

SNAP_DIR = Path(__file__).parent / "__snapshots__"


def _snapshot(name: str, actual: str) -> None:
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAP_DIR / name
    if path.exists():
        assert path.read_text(encoding="utf-8") == actual, f"snapshot mismatch: {name}"
    else:
        path.write_text(actual, encoding="utf-8")


def _capture_help(argv: list[str]) -> str:
    with pytest.raises(SystemExit):
        main(argv)
    return ""


def test_snapshot_completion_bash(capsys: pytest.CaptureFixture[str]) -> None:
    main(["completion", "--shell", "bash"])
    out, _ = capsys.readouterr()
    _snapshot("completion_bash.txt", out)


def test_snapshot_completion_zsh(capsys: pytest.CaptureFixture[str]) -> None:
    main(["completion", "--shell", "zsh"])
    out, _ = capsys.readouterr()
    _snapshot("completion_zsh.txt", out)


def test_snapshot_help_top_level(capsys: pytest.CaptureFixture[str]) -> None:
    _capture_help(["--help"])
    out, _ = capsys.readouterr()
    _snapshot("help_top_level.txt", out)


def test_snapshot_help_mission(capsys: pytest.CaptureFixture[str]) -> None:
    _capture_help(["mission", "--help"])
    out, _ = capsys.readouterr()
    _snapshot("help_mission.txt", out)


def test_snapshot_help_task(capsys: pytest.CaptureFixture[str]) -> None:
    _capture_help(["task", "--help"])
    out, _ = capsys.readouterr()
    _snapshot("help_task.txt", out)


def test_snapshot_version(capsys: pytest.CaptureFixture[str]) -> None:
    _capture_help(["--version"])
    out, _ = capsys.readouterr()
    _snapshot("version.txt", out)
