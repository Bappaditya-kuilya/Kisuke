"""Logging configuration for Kisuke.

Configures a single root logger. Secrets, tokens, and personal data are never
logged.
"""

from __future__ import annotations

import logging
import sys

_DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the Kisuke root logger.

    Idempotent: existing handlers are preserved across calls.
    """
    root = logging.getLogger("kisuke")
    root.setLevel(level)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
        root.addHandler(handler)
    return root
