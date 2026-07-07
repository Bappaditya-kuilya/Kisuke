"""Tests for Kisuke logging configuration."""

from __future__ import annotations

import logging

from kisuke.shared.logging import configure_logging


def test_configure_logging_returns_kisuke_logger() -> None:
    logger = configure_logging(logging.WARNING)

    assert logger.name == "kisuke"
    assert logger.level == logging.WARNING
    assert logger.handlers


def test_configure_logging_is_idempotent() -> None:
    first = configure_logging(logging.INFO)
    handler_count = len(first.handlers)

    second = configure_logging(logging.DEBUG)

    assert second is first
    assert len(second.handlers) == handler_count
