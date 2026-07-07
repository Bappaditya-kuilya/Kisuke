"""Tests for the Kisuke package foundation."""

from __future__ import annotations

import kisuke


def test_package_imports() -> None:
    assert kisuke.__version__ == "0.1.0"
