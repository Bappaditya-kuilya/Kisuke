"""Infrastructure validation package.

Pure Infrastructure layer: scans the Markdown repository, parses entities, and
validates them against the Domain Model (reusing the Domain's rule tables). It
never modifies repository contents.
"""

from __future__ import annotations

from .parser import IncrementalParser, ParseCache, ParseResult
from .report import IssueCode, IssueSeverity, ValidationIssue, ValidationReport
from .scanner import RepositoryScanner
from .schema import schema_issues
from .validator import RepositoryValidator

__all__ = [
    "IncrementalParser",
    "ParseCache",
    "ParseResult",
    "IssueCode",
    "IssueSeverity",
    "ValidationIssue",
    "ValidationReport",
    "RepositoryScanner",
    "schema_issues",
    "RepositoryValidator",
]
