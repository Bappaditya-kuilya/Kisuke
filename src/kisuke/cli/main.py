"""CLI entrypoint.

Parses arguments, builds the runtime context, dispatches to the matched
command handler, formats the result, and translates any failure into a
consistent exit code.
"""

from __future__ import annotations

import sys

from kisuke.cli.commands import build_context, build_parser
from kisuke.cli.errors import exit_code_for
from kisuke.cli.format import OutputFormatter


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ctx = build_context(args)
    try:
        result = args.func(args, ctx)
    except Exception as exc:  # noqa: BLE001 - top-level CLI boundary
        message, code = exit_code_for(exc)
        print(message, file=sys.stderr)
        return code
    OutputFormatter.emit(result, ctx.as_json, ctx.quiet)
    return 0


if __name__ == "__main__":
    sys.exit(main())
