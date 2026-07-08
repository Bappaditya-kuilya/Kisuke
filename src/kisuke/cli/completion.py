"""Shell completion architecture (prepared).

The CLI specification permits preparing shell-completion infrastructure without
requiring it. This module generates a bash/zsh completion script that completes
top-level subcommands. It is intentionally simple and offline; a full
per-option completer can be layered on later without changing the CLI contract.
"""

from __future__ import annotations

TOP_LEVEL_COMMANDS = (
    "init",
    "doctor",
    "status",
    "config",
    "resume",
    "mission",
    "project",
    "task",
    "knowledge",
    "cookbook",
    "decision",
    "meeting",
    "person",
    "resource",
    "review",
    "search",
    "sync",
    "plugin",
    "index",
    "completion",
    "validate",
)


def _bash_script() -> str:
    commands = " ".join(TOP_LEVEL_COMMANDS)
    return (
        "# bash completion for kisuke\n"
        "_kisuke() {\n"
        "    local cur prev\n"
        "    COMPREPLY=()\n"
        '    cur="${COMP_WORDS[COMP_CWORD]}"\n'
        '    if [ "$COMP_CWORD" -eq 1 ]; then\n'
        f'        COMPREPLY=( $(compgen -W "{commands}" -- "$cur") )\n'
        "        return 0\n"
        "    fi\n"
        "}\n"
        "complete -F _kisuke kisuke\n"
    )


def _zsh_script() -> str:
    commands = " ".join(TOP_LEVEL_COMMANDS)
    return (
        "# zsh completion for kisuke\n"
        "#compdef kisuke\n"
        f"_kisuke() {{ _arguments '1:command:(({commands}))' '*:: :_files' }}\n"
        "_kisuke\n"
    )


def emit_completion(shell: str) -> str:
    """Return a shell completion script for ``shell`` (bash or zsh)."""
    if shell == "zsh":
        return _zsh_script()
    return _bash_script()
