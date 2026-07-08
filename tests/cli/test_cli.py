"""End-to-end CLI tests.

Each test drives the CLI through :func:`kisuke.cli.main.main` against an isolated
repository, exercising the full adapter path (CLI -> Application -> Infrastructure).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kisuke.cli.main import main


def _run(capsys: pytest.CaptureFixture[str], argv: list[str]) -> tuple[int, str, str]:
    code = main(argv)
    out, err = capsys.readouterr()
    return code, out, err


def _create_and_id(capsys: pytest.CaptureFixture[str], argv: list[str]) -> str:
    code, out, _ = _run(capsys, argv + ["--json"])
    assert code == 0, out
    return json.loads(out)["id"]


def test_init(cli_env: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["init"])
    assert code == 0
    assert "Initialized repository" in out
    for folder in ("missions", "projects", "tasks"):
        assert (cli_env / folder).is_dir()


def test_init_idempotent(cli_env: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _run(capsys, ["init"])
    code, out, _ = _run(capsys, ["init"])
    assert code == 0
    assert "already initialized" in out


def test_status_empty(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["status"])
    assert code == 0
    assert "Repository:" in out
    assert "mission: 0" in out


def test_mission_create_and_list(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "Career"])
    code, out, _ = _run(capsys, ["mission", "list"])
    assert code == 0
    assert "Career" in out
    assert mid in out


def test_mission_show(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "Career"])
    code, out, _ = _run(capsys, ["mission", "show", mid])
    assert code == 0
    assert "Career" in out
    assert "id:" in out


def test_mission_archive(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "Career"])
    code, out, _ = _run(capsys, ["mission", "archive", mid])
    assert code == 0
    assert "Archived" in out
    code, out, _ = _run(capsys, ["mission", "show", mid, "--json"])
    assert code == 0
    assert json.loads(out)["status"] == "Archived"


def test_project_requires_mission(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, err = _run(capsys, ["project", "create", "--title", "X"])
    assert code == 2
    assert "requires --mission" in err


def test_project_create_and_open(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "M"])
    pid = _create_and_id(capsys, ["project", "create", "--title", "P", "--mission", mid])
    code, out, _ = _run(capsys, ["project", "open", pid])
    assert code == 0
    assert out.strip().endswith(f"{pid}.md")


def test_task_workflow(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "M"])
    pid = _create_and_id(capsys, ["project", "create", "--title", "P", "--mission", mid])
    tid = _create_and_id(capsys, ["task", "add", "--title", "T", "--project", pid])

    code, out, _ = _run(capsys, ["task", "list", "--project", pid])
    assert code == 0 and tid in out

    code, out, _ = _run(capsys, ["task", "next", "--project", pid])
    assert code == 0 and tid in out

    code, out, _ = _run(capsys, ["task", "done", tid])
    assert code == 0
    code, out, _ = _run(capsys, ["task", "list", "--project", pid, "--status", "Done"])
    assert tid in out


def test_task_move(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "M"])
    p1 = _create_and_id(capsys, ["project", "create", "--title", "P1", "--mission", mid])
    p2 = _create_and_id(capsys, ["project", "create", "--title", "P2", "--mission", mid])
    tid = _create_and_id(capsys, ["task", "add", "--title", "T", "--project", p1])
    code, out, _ = _run(capsys, ["task", "move", tid, "--project", p2])
    assert code == 0
    code, out, _ = _run(capsys, ["task", "list", "--project", p2])
    assert tid in out
    code, out, _ = _run(capsys, ["task", "list", "--project", p1])
    assert tid not in out


def test_knowledge_add_open(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "M"])
    pid = _create_and_id(capsys, ["project", "create", "--title", "P", "--mission", mid])
    kid = _create_and_id(
        capsys, ["knowledge", "add", "--title", "K", "--project", pid, "--summary", "s"]
    )
    code, out, _ = _run(capsys, ["knowledge", "open", kid])
    assert code == 0 and out.strip().endswith(f"{kid}.md")


def test_cookbook_search_open(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    cid = _create_and_id(
        capsys, ["cookbook", "add", "--title", "Git tricks", "--content", "rebase"]
    )
    code, out, _ = _run(capsys, ["cookbook", "search", "rebase"])
    assert code == 0 and cid in out
    code, out, _ = _run(capsys, ["cookbook", "open", cid])
    assert code == 0 and out.strip().endswith(f"{cid}.md")


def test_decision_add_list_show(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "M"])
    pid = _create_and_id(capsys, ["project", "create", "--title", "P", "--mission", mid])
    did = _create_and_id(
        capsys, ["decision", "add", "--title", "D", "--project", pid, "--decision", "use x"]
    )
    code, out, _ = _run(capsys, ["decision", "list"])
    assert code == 0 and did in out
    code, out, _ = _run(capsys, ["decision", "show", did])
    assert code == 0 and "use x" in out


def test_meeting_add_today_list(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["meeting", "add", "--title", "Sync", "--date", "2099-01-01"])
    code, out, _ = _run(capsys, ["meeting", "list"])
    assert code == 0 and mid in out
    code, out, _ = _run(capsys, ["meeting", "today"])
    assert code == 0
    assert "No meetings scheduled today" in out


def test_person_add_list_show(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pid = _create_and_id(capsys, ["person", "add", "--title", "Ada", "--role", "Mentor"])
    code, out, _ = _run(capsys, ["person", "list"])
    assert code == 0 and pid in out
    code, out, _ = _run(capsys, ["person", "show", pid])
    assert code == 0 and "Ada" in out


def test_resource_add_list_open(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rid = _create_and_id(capsys, ["resource", "add", "--title", "Docs", "--url", "https://x"])
    code, out, _ = _run(capsys, ["resource", "list"])
    assert code == 0 and rid in out
    code, out, _ = _run(capsys, ["resource", "open", rid])
    assert code == 0 and out.strip().endswith(f"{rid}.md")


def test_resume(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "M"])
    _create_and_id(capsys, ["project", "create", "--title", "P", "--mission", mid])
    code, out, _ = _run(capsys, ["resume"])
    assert code == 0
    assert "Resume" in out


def test_review_commands(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    for kind in ("morning", "weekly", "monthly", "quarterly"):
        code, out, _ = _run(capsys, ["review", kind])
        assert code == 0, kind
        assert "Review" in out


def test_search(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mid = _create_and_id(capsys, ["mission", "create", "--title", "UniqueMissionName"])
    code, out, _ = _run(capsys, ["search", "UniqueMissionName"])
    assert code == 0 and mid in out


def test_validate(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["validate"])
    assert code == 0
    assert "Status: VALID" in out


def test_doctor(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["doctor"])
    assert code == 0
    assert "[PASS] repository" in out
    assert "[PASS] markdown" in out


def test_index_build_update_clean(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["index", "build"])
    assert code == 0 and "Built index" in out
    code, out, _ = _run(capsys, ["index", "update"])
    assert code == 0 and "Updated index" in out
    code, out, _ = _run(capsys, ["index", "clean"])
    assert code == 0 and "Cleaned index" in out


def test_sync(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["sync"])
    assert code == 0 and "Synced index" in out


def test_plugin_lifecycle(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, _ = _run(capsys, ["plugin", "install", "demo", "--source", "git"])
    assert code == 0
    code, out, _ = _run(capsys, ["plugin", "list"])
    assert code == 0 and "demo" in out
    code, out, _ = _run(capsys, ["plugin", "update", "demo"])
    assert code == 0 and "demo" in out
    code, _, _ = _run(capsys, ["plugin", "remove", "demo"])
    assert code == 0
    code, out, _ = _run(capsys, ["plugin", "list"])
    assert code == 0 and "No plugins" in out


def test_plugin_remove_missing(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, err = _run(capsys, ["plugin", "remove", "nope"])
    assert code == 3
    assert "not installed" in err


def test_config_get_set(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["config", "set", "log_level", "DEBUG"])
    assert code == 0
    code, out, _ = _run(capsys, ["config", "get", "log_level"])
    assert code == 0 and "DEBUG" in out


def test_config_set_unknown_key(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, err = _run(capsys, ["config", "set", "bogus", "x"])
    assert code == 2
    assert "unknown config key" in err


def test_config_edit(
    runner: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("EDITOR", "true")
    code, out, _ = _run(capsys, ["config", "edit"])
    assert code == 0
    assert "Opened" in out


def test_json_flag_positions(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _create_and_id(capsys, ["mission", "create", "--title", "M"])
    code, out, _ = _run(capsys, ["--json", "mission", "list"])
    assert code == 0
    assert isinstance(json.loads(out), list)
    code, out, _ = _run(capsys, ["mission", "list", "--json"])
    assert code == 0
    assert isinstance(json.loads(out), list)


def test_exit_not_found(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, err = _run(capsys, ["mission", "show", "00000000-0000-0000-0000-000000000000"])
    assert code == 3
    assert "No mission" in err


def test_exit_bad_uuid(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, err = _run(capsys, ["mission", "show", "not-a-uuid"])
    assert code == 4
    assert "Invalid EntityId" in err


def test_exit_missing_args(runner: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, _ = _run(capsys, ["project", "create", "--title", "X"])
    assert code == 2


def test_help_top_level(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out, _ = capsys.readouterr()
    assert "usage:" in out
    assert "mission" in out


def test_help_subcommand(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["mission", "--help"])
    assert exc.value.code == 0
    out, _ = capsys.readouterr()
    assert "create" in out
    assert "list" in out


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    out, _ = capsys.readouterr()
    assert "0.1.0" in out


def test_completion(capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["completion", "--shell", "bash"])
    assert code == 0
    assert "complete -F _kisuke kisuke" in out
