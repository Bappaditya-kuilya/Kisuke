"""CLI output formatting.

Every command handler returns a :class:`Result` carrying both a human-readable
string and a JSON-serializable payload. The formatter emits one or the other
based on the global ``--json`` flag, keeping output script-friendly and
deterministic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class Result:
    """The outcome of a command, in both human and machine form."""

    human: str
    json: object = field(default_factory=dict)


class OutputFormatter:
    """Renders a :class:`Result` to stdout."""

    @staticmethod
    def emit(result: Result, as_json: bool, quiet: bool = False) -> None:
        if quiet:
            return
        if as_json:
            print(json.dumps(result.json, indent=2, default=str, sort_keys=False))
        elif result.human:
            print(result.human)
