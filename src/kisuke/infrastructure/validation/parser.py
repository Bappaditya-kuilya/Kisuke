"""Incremental Markdown parser for repository validation.

Reads entity files and converts them to Domain entities. Parsed results are
cached by file identity (modification time + size) so that unchanged files are
not re-parsed on subsequent validation passes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kisuke.domain.entities import Entity
from kisuke.infrastructure.storage.frontmatter import loads_yaml, split_markdown
from kisuke.infrastructure.storage.serializer import markdown_to_entity


@dataclass
class ParseResult:
    """Outcome of parsing one file."""

    path: Path
    fm: dict[str, Any] | None = None
    entity: Entity | None = None
    error: str | None = None


class ParseCache:
    """In-memory cache keyed by path and file identity."""

    def __init__(self) -> None:
        self._store: dict[Path, tuple[int, int, ParseResult]] = {}

    def get(self, path: Path, mtime_ns: int, size: int) -> ParseResult | None:
        entry = self._store.get(path)
        if entry is not None and entry[0] == mtime_ns and entry[1] == size:
            return entry[2]
        return None

    def put(self, path: Path, mtime_ns: int, size: int, result: ParseResult) -> None:
        self._store[path] = (mtime_ns, size, result)


class IncrementalParser:
    """Parses entity files, caching unchanged ones."""

    def __init__(self, cache: ParseCache | None = None) -> None:
        self.cache = cache or ParseCache()
        self.parse_count = 0

    def parse_file(self, path: Path) -> ParseResult:
        stat = path.stat()
        cached = self.cache.get(path, stat.st_mtime_ns, stat.st_size)
        if cached is not None:
            return cached
        self.parse_count += 1
        result = self._parse(path)
        self.cache.put(path, stat.st_mtime_ns, stat.st_size, result)
        return result

    @staticmethod
    def _parse(path: Path) -> ParseResult:
        try:
            text = path.read_text(encoding="utf-8")
            fm_text, _ = split_markdown(text)
            fm = loads_yaml(fm_text)
        except Exception as exc:  # noqa: BLE001 - surface any read/parse failure
            return ParseResult(path=path, error=f"cannot read frontmatter: {exc}")
        try:
            entity = markdown_to_entity(text)
        except Exception as exc:  # noqa: BLE001 - surface any construction failure
            return ParseResult(path=path, fm=fm, error=f"cannot parse entity: {exc}")
        return ParseResult(path=path, fm=fm, entity=entity)
