"""CLI exit codes and exception mapping.

Centralizes the exit-code contract from the CLI specification so every command
handler can raise domain/infrastructure exceptions and have them translated into
consistent, helpful CLI exit codes.
"""

from __future__ import annotations

from enum import IntEnum


class ExitCode(IntEnum):
    """Exit codes defined by the CLI specification."""

    SUCCESS = 0
    GENERAL = 1
    INVALID_ARGS = 2
    NOT_FOUND = 3
    VALIDATION = 4
    PERMISSION = 5


class CliError(Exception):
    """An explicit CLI failure carrying its own exit code."""

    def __init__(self, message: str, code: ExitCode = ExitCode.GENERAL) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


def exit_code_for(exc: Exception) -> tuple[str, int]:
    """Map an exception to ``(message, exit_code)``."""
    from kisuke.domain.exceptions import ValidationError
    from kisuke.infrastructure.storage.interfaces import RepositoryError

    if isinstance(exc, CliError):
        return exc.message, int(exc.code)
    if isinstance(exc, RepositoryError):
        return str(exc), int(ExitCode.NOT_FOUND)
    if isinstance(exc, ValidationError):
        problems = getattr(exc, "problems", None)
        message = "; ".join(problems) if isinstance(problems, list) and problems else str(exc)
        return message, int(ExitCode.VALIDATION)
    if isinstance(exc, FileNotFoundError):
        return str(exc), int(ExitCode.NOT_FOUND)
    if isinstance(exc, PermissionError):
        return str(exc), int(ExitCode.PERMISSION)
    if isinstance(exc, ValueError):
        return str(exc), int(ExitCode.INVALID_ARGS)
    if isinstance(exc, KeyError):
        return f"missing key: {exc}", int(ExitCode.INVALID_ARGS)
    return str(exc), int(ExitCode.GENERAL)
