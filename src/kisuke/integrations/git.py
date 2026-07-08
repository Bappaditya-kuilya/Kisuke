"""Git integration.

Read-only repository introspection plus an explicit, user-approved commit
helper. Git remains the system of record: this adapter never rewrites history
or pushes, and it only writes when ``commit`` is called explicitly. All reads
degrade gracefully when Git is absent or the directory is not a repository.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

from kisuke.integrations.base import BaseIntegration


class GitIntegration(BaseIntegration):
    """Integrate with a local Git repository."""

    name = "git"
    category = "development"
    description = "Local Git repository detection, branch, commits, and status."

    def __init__(self, root: Path, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)
        self.root = Path(root)

    # ------------------------------------------------------------------
    # Availability
    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        return shutil.which("git") is not None and self.is_git_repo()

    def is_git_repo(self) -> bool:
        result = self._run(["rev-parse", "--is-inside-work-tree"])
        return result.returncode == 0 and result.stdout.strip() == "true"

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------
    def current_branch(self) -> str | None:
        result = self._run(["rev-parse", "--abbrev-ref", "HEAD"])
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None

    def recent_commits(self, count: int = 10) -> list[dict[str, str]]:
        fmt = "%H%x1f%an%x1f%ad%x1f%s"
        result = self._run(["log", f"-n{count}", "--date=short", f"--pretty=format:{fmt}"])
        if result.returncode != 0:
            return []
        commits: list[dict[str, str]] = []
        for line in result.stdout.splitlines():
            parts = line.split("\x1f")
            if len(parts) == 4:
                commits.append(
                    {"hash": parts[0], "author": parts[1], "date": parts[2], "message": parts[3]}
                )
        return commits

    def status(self) -> dict[str, Any]:
        result = self._run(["status", "--porcelain=v1", "--branch"])
        if result.returncode != 0:
            return {"clean": True, "changes": []}
        changes = [
            line
            for line in result.stdout.splitlines()
            if line.strip() and not line.startswith("## ")
        ]
        return {"clean": len(changes) == 0, "changes": changes}

    def snapshot(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "is_repo": self.is_git_repo(),
            "branch": self.current_branch(),
            "commits": self.recent_commits(self.option("commit_count", 10)),
            "status": self.status(),
        }

    # ------------------------------------------------------------------
    # Writes (explicit, user-approved only)
    # ------------------------------------------------------------------
    def commit(self, message: str, paths: list[str] | None = None) -> str | None:
        """Stage and commit the given paths (or all) with a user-supplied message."""
        add_targets = paths if paths else ["-A"]
        add = self._run(["add", *add_targets])
        if add.returncode != 0:
            raise RuntimeError(f"git add failed: {add.stderr.strip()}")
        commit = self._run(["commit", "-m", message])
        if commit.returncode != 0:
            return None
        return commit.stdout.strip() or "committed"

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=str(self.root),
            capture_output=True,
            text=True,
            check=False,
        )
