"""CLI command definitions.

Builds the argparse command tree documented in ``docs/engineering/08-cli-spec.md``
and wires each leaf command to an Application service. Handlers contain no
business logic: they translate parsed arguments into service calls and render
:class:`Result` objects.
"""

from __future__ import annotations

import argparse
import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kisuke.application.config_app import ConfigService, resolve_config
from kisuke.application.doctor import DoctorService
from kisuke.application.entities import EntityService, entity_to_dict
from kisuke.application.index_app import IndexService
from kisuke.application.plugins import PluginService
from kisuke.application.resume_app import ResumeApp
from kisuke.application.reviews import ReviewService
from kisuke.application.search_app import SearchService
from kisuke.application.tasks import TaskService
from kisuke.application.validation_app import ValidateService
from kisuke.application.workspace import (
    init_repository,
    repository_status,
    resolve_repo_root,
)
from kisuke.cli.completion import emit_completion
from kisuke.cli.errors import CliError, ExitCode
from kisuke.cli.format import Result
from kisuke.domain.entities import Entity
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import EntityType
from kisuke.infrastructure.storage.repository import FOLDER_NAMES, FileRepository
from kisuke.infrastructure.storage.serializer import entity_to_markdown
from kisuke.shared.config import Config


@dataclass
class CliContext:
    """Resolved runtime context shared by all command handlers."""

    repo_root: Path
    config: Config
    db_path: Path
    settings_path: Path
    registry_path: Path
    last_focus_path: Path
    as_json: bool
    quiet: bool
    verbose: bool

    def repo(self) -> FileRepository:
        return FileRepository(self.repo_root)


def _entity_params(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "title": getattr(args, "title", None),
        "description": getattr(args, "description", None),
        "priority": getattr(args, "priority", None),
        "summary": getattr(args, "summary", None),
        "content": getattr(args, "content", None),
        "category": getattr(args, "category", None),
        "decision": getattr(args, "decision", None),
        "reason": getattr(args, "reason", None),
        "alternatives": getattr(args, "alternatives", None),
        "date": getattr(args, "date", None),
        "role": getattr(args, "role", None),
        "organization": getattr(args, "organization", None),
        "email": getattr(args, "email", None),
        "notes": getattr(args, "notes", None),
        "resource_type": getattr(args, "resource_type", None),
        "url": getattr(args, "url", None),
        "due_date": getattr(args, "due_date", None),
        "estimated_time": getattr(args, "estimated_time", None),
        "mission": getattr(args, "mission", None),
        "project": getattr(args, "project", None),
        "people": getattr(args, "people", None),
        "projects": getattr(args, "projects", None),
        "tasks": getattr(args, "tasks", None),
        "decisions": getattr(args, "decisions", None),
        "resources": getattr(args, "resources", None),
        "tags": getattr(args, "tags", None),
        "references": getattr(args, "references", None),
        "links": getattr(args, "links", None),
    }


# ---------------------------------------------------------------------------
# Generic entity handlers
# ---------------------------------------------------------------------------
def cmd_entity_create(args: argparse.Namespace, ctx: CliContext, et: EntityType) -> Result:
    entity = EntityService(ctx.repo()).create(et, _entity_params(args))
    path = ctx.repo_root / FOLDER_NAMES[et] / f"{entity.id}.md"
    human = f"Created {et.value} {entity.id}\n  title: {entity.title}\n  path:  {path}"
    return Result(human, entity_to_dict(entity))


def cmd_entity_list(args: argparse.Namespace, ctx: CliContext, et: EntityType) -> Result:
    entities = EntityService(ctx.repo()).list(et)
    if not entities:
        return Result(f"No {et.value} entities.", [entity_to_dict(e) for e in entities])
    lines = [f"{et.value.title()}s:"]
    for entity in entities:
        lines.append(f"  {entity.id}  {entity.title}  [{entity.status}]")
    return Result("\n".join(lines), [entity_to_dict(e) for e in entities])


def cmd_entity_show(args: argparse.Namespace, ctx: CliContext, et: EntityType) -> Result:
    entity = EntityService(ctx.repo()).show(et, EntityId.from_string(args.id))
    return Result(entity_to_markdown(entity), entity_to_dict(entity))


def cmd_entity_archive(args: argparse.Namespace, ctx: CliContext, et: EntityType) -> Result:
    updated = EntityService(ctx.repo()).archive(et, EntityId.from_string(args.id))
    return Result(f"Archived {et.value} {args.id}", entity_to_dict(updated))


def cmd_entity_open(args: argparse.Namespace, ctx: CliContext, et: EntityType) -> Result:
    eid = EntityId.from_string(args.id)
    path = EntityService(ctx.repo()).path(et, eid)
    if not path.exists():
        raise CliError(f"entity file not found: {path}", ExitCode.NOT_FOUND)
    return Result(str(path), {"type": et.value, "id": str(eid), "path": str(path)})


# ---------------------------------------------------------------------------
# Task handlers
# ---------------------------------------------------------------------------
def cmd_task_add(args: argparse.Namespace, ctx: CliContext) -> Result:
    task = TaskService(ctx.repo()).add(_entity_params(args))
    return Result(f"Added task {task.id}\n  title: {task.title}", entity_to_dict(task))


def cmd_task_list(args: argparse.Namespace, ctx: CliContext) -> Result:
    tasks = TaskService(ctx.repo()).list(project=args.project, status=args.status)
    if not tasks:
        return Result("No tasks.", [entity_to_dict(t) for t in tasks])
    lines = ["Tasks:"]
    for task in tasks:
        lines.append(f"  {task.id}  {task.title}  [{task.status}]")
    return Result("\n".join(lines), [entity_to_dict(t) for t in tasks])


def cmd_task_next(args: argparse.Namespace, ctx: CliContext) -> Result:
    task = TaskService(ctx.repo()).next(project=args.project)
    if task is None:
        return Result("No next task.", {"next_action": None})
    return Result(f"Next: {task.title} ({task.id})", entity_to_dict(task))


def cmd_task_done(args: argparse.Namespace, ctx: CliContext) -> Result:
    task = TaskService(ctx.repo()).done(EntityId.from_string(args.id))
    return Result(f"Done: {task.title} ({task.id})", entity_to_dict(task))


def cmd_task_move(args: argparse.Namespace, ctx: CliContext) -> Result:
    task = TaskService(ctx.repo()).move(EntityId.from_string(args.id), args.project)
    return Result(f"Moved {task.id} to project {args.project}", entity_to_dict(task))


# ---------------------------------------------------------------------------
# Search / index / sync
# ---------------------------------------------------------------------------
def _search_result(results: list[Any], query: str) -> Result:
    if not results:
        return Result("No results.", {"query": query, "results": []})
    lines = [f"Search: {query}", ""]
    payload = []
    for r in results:
        lines.append(f"  {r.score:.2f}  {r.entity_id}  [{r.entity_type}]  {r.title}")
        payload.append(
            {
                "entity_id": r.entity_id,
                "entity_type": r.entity_type,
                "title": r.title,
                "owner": r.owner,
                "status": r.status,
                "score": r.score,
            }
        )
    return Result("\n".join(lines), {"query": query, "results": payload})


def cmd_search(args: argparse.Namespace, ctx: CliContext) -> Result:
    entity_type: str | None = None
    for flag, name in (
        ("project", "project"),
        ("cookbook", "cookbook"),
        ("knowledge", "knowledge"),
        ("decision", "decision"),
        ("resource", "resource"),
        ("person", "person"),
    ):
        if getattr(args, flag, False):
            entity_type = name
            break
    results = SearchService(ctx.repo_root, ctx.db_path).search(args.query, entity_type=entity_type)
    return _search_result(results, args.query)


def cmd_cookbook_search(args: argparse.Namespace, ctx: CliContext) -> Result:
    results = SearchService(ctx.repo_root, ctx.db_path).search(args.query, entity_type="cookbook")
    return _search_result(results, args.query)


def cmd_sync(args: argparse.Namespace, ctx: CliContext) -> Result:
    indexed = IndexService(ctx.repo_root, ctx.db_path).update()
    return Result(f"Synced index ({indexed} entities updated)", {"updated": indexed})


def cmd_index_build(args: argparse.Namespace, ctx: CliContext) -> Result:
    indexed = IndexService(ctx.repo_root, ctx.db_path).build()
    return Result(f"Built index ({indexed} entities)", {"indexed": indexed})


def cmd_index_update(args: argparse.Namespace, ctx: CliContext) -> Result:
    indexed = IndexService(ctx.repo_root, ctx.db_path).update()
    return Result(f"Updated index ({indexed} entities)", {"updated": indexed})


def cmd_index_clean(args: argparse.Namespace, ctx: CliContext) -> Result:
    removed = IndexService(ctx.repo_root, ctx.db_path).clean()
    return Result(
        "Cleaned index." if removed else "No index to clean.",
        {"removed": removed},
    )


# ---------------------------------------------------------------------------
# Resume / review
# ---------------------------------------------------------------------------
def _render_resume(result: Any) -> str:
    def ident(entity: Entity | None) -> str:
        return f"{entity.title} ({entity.id})" if entity is not None else "—"

    lines = [
        "Resume",
        "======",
        "",
        f"Mission: {ident(result.mission)}",
        f"Project: {ident(result.project)}",
        f"Next Action: {ident(result.next_action)}",
        "",
        _list_section("Tasks", result.related_tasks),
        _list_section("Knowledge", result.knowledge),
        _list_section("Decisions", result.decisions),
        _list_section("Meetings", result.meetings),
        _list_section("Resources", result.resources),
        _list_section("People", result.people),
        _list_section("Reviews", result.reviews),
    ]
    return "\n".join(lines)


def _list_section(title: str, items: list[Entity]) -> str:
    lines = [f"{title} ({len(items)}):"]
    for entity in items:
        lines.append(f"  - {entity.title} ({entity.id}) [{entity.status}]")
    return "\n".join(lines)


def cmd_resume(args: argparse.Namespace, ctx: CliContext) -> Result:
    result = ResumeApp(ctx.repo_root, ctx.db_path, ctx.last_focus_path).resume(
        mission=args.mission, project=args.project, last=args.last
    )
    return Result(_render_resume(result), result.to_dict())


def cmd_review_morning(args: argparse.Namespace, ctx: CliContext) -> Result:
    report = ReviewService(ctx.repo_root, ctx.db_path).morning()
    return Result(report.markdown, report.data)


def cmd_review_period(args: argparse.Namespace, ctx: CliContext, kind: str) -> Result:
    report = ReviewService(ctx.repo_root, ctx.db_path).period(kind)
    return Result(report.markdown, report.data)


# ---------------------------------------------------------------------------
# Config / doctor / status / init
# ---------------------------------------------------------------------------
def cmd_init(args: argparse.Namespace, ctx: CliContext) -> Result:
    created = init_repository(ctx.repo_root)
    if created:
        human = (
            "Initialized repository at "
            + str(ctx.repo_root)
            + "\n"
            + "\n".join("  created " + c for c in created)
        )
    else:
        human = "Repository already initialized at " + str(ctx.repo_root)
    return Result(human, {"root": str(ctx.repo_root), "created": created})


def cmd_status(args: argparse.Namespace, ctx: CliContext) -> Result:
    status = repository_status(ctx.repo_root)
    counts = status["counts"]
    assert isinstance(counts, dict)
    lines = [
        "Repository: " + str(ctx.repo_root),
        "Initialized: " + ("yes" if status["initialized"] else "no"),
        "",
        "Entities:",
    ]
    for key, value in counts.items():
        lines.append(f"  {key}: {value}")
    return Result("\n".join(lines), status)


def cmd_doctor(args: argparse.Namespace, ctx: CliContext) -> Result:
    checks = DoctorService(ctx.repo_root, ctx.config, ctx.db_path).run()
    lines = ["Doctor", ""]
    ok_all = True
    for check in checks:
        ok_all = ok_all and check.ok
        lines.append(f"[{'PASS' if check.ok else 'FAIL'}] {check.name}: {check.detail}")
    data = [{"name": c.name, "ok": c.ok, "detail": c.detail} for c in checks]
    return Result("\n".join(lines), {"checks": data, "ok": ok_all})


def cmd_config_get(args: argparse.Namespace, ctx: CliContext) -> Result:
    view = ConfigService(ctx.settings_path).get(args.key)
    if args.key:
        human = f"{args.key} = {view.get(args.key)}"
    else:
        human = "\n".join(f"{k} = {v}" for k, v in view.items())
    return Result(human, view)


def cmd_config_set(args: argparse.Namespace, ctx: CliContext) -> Result:
    result = ConfigService(ctx.settings_path).set(args.key, args.value)
    return Result(f"{args.key} = {args.value}", result)


def cmd_config_edit(args: argparse.Namespace, ctx: CliContext) -> Result:
    path = ConfigService(ctx.settings_path).edit()
    return Result(f"Opened {path} in $EDITOR", {"path": str(path)})


# ---------------------------------------------------------------------------
# Plugin
# ---------------------------------------------------------------------------
def cmd_plugin_list(args: argparse.Namespace, ctx: CliContext) -> Result:
    plugins = PluginService(ctx.registry_path).list_plugins()
    if not plugins:
        return Result("No plugins installed.", {"plugins": []})
    lines = ["Plugins:"]
    payload = []
    for plugin in plugins:
        lines.append(f"  {plugin.name}  ({plugin.source or 'no source'})")
        payload.append({"name": plugin.name, "source": plugin.source})
    return Result("\n".join(lines), {"plugins": payload})


def cmd_plugin_install(args: argparse.Namespace, ctx: CliContext) -> Result:
    plugin = PluginService(ctx.registry_path).install(args.name, args.source)
    return Result(f"Installed plugin {plugin.name}", {"name": plugin.name, "source": plugin.source})


def cmd_plugin_remove(args: argparse.Namespace, ctx: CliContext) -> Result:
    removed = PluginService(ctx.registry_path).remove(args.name)
    if not removed:
        raise CliError(f"plugin not installed: {args.name}", ExitCode.NOT_FOUND)
    return Result(f"Removed plugin {args.name}", {"name": args.name, "removed": True})


def cmd_plugin_update(args: argparse.Namespace, ctx: CliContext) -> Result:
    plugins = PluginService(ctx.registry_path).update(args.name)
    if not plugins:
        return Result("No plugins to update.", {"plugins": []})
    lines = ["Updated plugins:"]
    payload = []
    for plugin in plugins:
        lines.append(f"  {plugin.name}")
        payload.append({"name": plugin.name, "source": plugin.source})
    return Result("\n".join(lines), {"plugins": payload})


# ---------------------------------------------------------------------------
# Completion
# ---------------------------------------------------------------------------
def cmd_completion(args: argparse.Namespace, ctx: CliContext) -> Result:
    script = emit_completion(args.shell)
    return Result(script, {"shell": args.shell})


def cmd_validate(args: argparse.Namespace, ctx: CliContext) -> Result:
    report = ValidateService(ctx.repo_root).validate()
    human = report.render_text()
    data = [i.__dict__ for i in report.issues]
    return Result(human, {"valid": report.is_valid(), "issues": data})


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------
def _add_create_flags(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("--title", required=True)
    sub.add_argument("--description")
    sub.add_argument("--priority")
    sub.add_argument("--summary")
    sub.add_argument("--content")
    sub.add_argument("--category")
    sub.add_argument("--decision")
    sub.add_argument("--reason")
    sub.add_argument("--alternatives")
    sub.add_argument("--date")
    sub.add_argument("--role")
    sub.add_argument("--organization")
    sub.add_argument("--email")
    sub.add_argument("--notes")
    sub.add_argument("--resource-type", dest="resource_type")
    sub.add_argument("--url")
    sub.add_argument("--due-date", dest="due_date")
    sub.add_argument("--estimated-time", dest="estimated_time")
    sub.add_argument("--mission")
    sub.add_argument("--project")
    sub.add_argument("--people", nargs="*")
    sub.add_argument("--projects", nargs="*")
    sub.add_argument("--tasks", nargs="*")
    sub.add_argument("--decisions", nargs="*")
    sub.add_argument("--resources", nargs="*")
    sub.add_argument("--tags", nargs="*")
    sub.add_argument("--references", nargs="*")
    sub.add_argument("--links", nargs="*")


def _entity_group(
    parent: Any,
    name: str,
    et: EntityType,
    create: bool,
    open_cmd: bool,
    archive: bool,
    show: bool,
    create_verb: str = "create",
) -> None:
    group = parent.add_parser(name, parents=[_common])
    subs = group.add_subparsers(dest="subcommand", required=True)
    if create:
        c = subs.add_parser(create_verb, parents=[_common])
        _add_create_flags(c)
        c.set_defaults(func=functools.partial(cmd_entity_create, et=et))
    list_sub = subs.add_parser("list", parents=[_common])
    list_sub.set_defaults(func=functools.partial(cmd_entity_list, et=et))
    if show:
        s = subs.add_parser("show", parents=[_common])
        s.add_argument("id")
        s.set_defaults(func=functools.partial(cmd_entity_show, et=et))
    if open_cmd:
        o = subs.add_parser("open", parents=[_common])
        o.add_argument("id")
        o.set_defaults(func=functools.partial(cmd_entity_open, et=et))
    if archive:
        a = subs.add_parser("archive", parents=[_common])
        a.add_argument("id")
        a.set_defaults(func=functools.partial(cmd_entity_archive, et=et))


def build_parser() -> argparse.ArgumentParser:
    """Build the full kisuke argument parser."""
    global _common
    _common = argparse.ArgumentParser(add_help=False)
    _common.add_argument(
        "--json", action="store_true", default=argparse.SUPPRESS, help="machine-readable output"
    )
    _common.add_argument(
        "--quiet", action="store_true", default=argparse.SUPPRESS, help="suppress output"
    )
    _common.add_argument(
        "--verbose", action="store_true", default=argparse.SUPPRESS, help="verbose logging"
    )

    parser = argparse.ArgumentParser(
        prog="kisuke",
        description="Kisuke: local-first context reconstruction engine.",
        parents=[_common],
    )
    parser.add_argument("--version", action="version", version=_version())
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser("init", parents=[_common])
    init_p.set_defaults(func=cmd_init)

    doctor_p = subparsers.add_parser("doctor", parents=[_common])
    doctor_p.set_defaults(func=cmd_doctor)

    status_p = subparsers.add_parser("status", parents=[_common])
    status_p.set_defaults(func=cmd_status)

    # config
    config_p = subparsers.add_parser("config", parents=[_common])
    config_subs = config_p.add_subparsers(dest="subcommand", required=True)
    cg = config_subs.add_parser("get", parents=[_common])
    cg.add_argument("key", nargs="?")
    cg.set_defaults(func=cmd_config_get)
    cs = config_subs.add_parser("set", parents=[_common])
    cs.add_argument("key")
    cs.add_argument("value")
    cs.set_defaults(func=cmd_config_set)
    ce = config_subs.add_parser("edit", parents=[_common])
    ce.set_defaults(func=cmd_config_edit)

    # resume
    resume_p = subparsers.add_parser("resume", parents=[_common])
    resume_p.add_argument("--mission")
    resume_p.add_argument("--project")
    resume_p.add_argument("--last", action="store_true")
    resume_p.set_defaults(func=cmd_resume)

    # entity groups
    _entity_group(
        subparsers,
        "mission",
        EntityType.MISSION,
        create=True,
        open_cmd=False,
        archive=True,
        show=True,
    )
    _entity_group(
        subparsers,
        "project",
        EntityType.PROJECT,
        create=True,
        open_cmd=True,
        archive=True,
        show=True,
    )
    _entity_group(
        subparsers,
        "knowledge",
        EntityType.KNOWLEDGE,
        create=True,
        create_verb="add",
        open_cmd=True,
        archive=False,
        show=False,
    )
    _entity_group(
        subparsers,
        "decision",
        EntityType.DECISION,
        create=True,
        create_verb="add",
        open_cmd=False,
        archive=False,
        show=True,
    )
    _entity_group(
        subparsers,
        "person",
        EntityType.PERSON,
        create=True,
        create_verb="add",
        open_cmd=False,
        archive=False,
        show=True,
    )
    _entity_group(
        subparsers,
        "resource",
        EntityType.RESOURCE,
        create=True,
        create_verb="add",
        open_cmd=True,
        archive=False,
        show=False,
    )

    # task
    task_p = subparsers.add_parser("task", parents=[_common])
    task_subs = task_p.add_subparsers(dest="subcommand", required=True)
    ta = task_subs.add_parser("add", parents=[_common])
    _add_create_flags(ta)
    ta.set_defaults(func=cmd_task_add)
    tl = task_subs.add_parser("list", parents=[_common])
    tl.add_argument("--project")
    tl.add_argument("--status")
    tl.set_defaults(func=cmd_task_list)
    tn = task_subs.add_parser("next", parents=[_common])
    tn.add_argument("--project")
    tn.set_defaults(func=cmd_task_next)
    td = task_subs.add_parser("done", parents=[_common])
    td.add_argument("id")
    td.set_defaults(func=cmd_task_done)
    tm = task_subs.add_parser("move", parents=[_common])
    tm.add_argument("id")
    tm.add_argument("--project", required=True)
    tm.set_defaults(func=cmd_task_move)

    # cookbook
    cookbook_p = subparsers.add_parser("cookbook", parents=[_common])
    cookbook_subs = cookbook_p.add_subparsers(dest="subcommand", required=True)
    cba = cookbook_subs.add_parser("add", parents=[_common])
    _add_create_flags(cba)
    cba.set_defaults(func=functools.partial(cmd_entity_create, et=EntityType.COOKBOOK))
    cbs = cookbook_subs.add_parser("search", parents=[_common])
    cbs.add_argument("query")
    cbs.set_defaults(func=cmd_cookbook_search)
    cbo = cookbook_subs.add_parser("open", parents=[_common])
    cbo.add_argument("id")
    cbo.set_defaults(func=functools.partial(cmd_entity_open, et=EntityType.COOKBOOK))

    # meeting
    meeting_p = subparsers.add_parser("meeting", parents=[_common])
    meeting_subs = meeting_p.add_subparsers(dest="subcommand", required=True)
    ma = meeting_subs.add_parser("add", parents=[_common])
    _add_create_flags(ma)
    ma.set_defaults(func=functools.partial(cmd_entity_create, et=EntityType.MEETING))
    mt = meeting_subs.add_parser("today", parents=[_common])
    mt.set_defaults(func=cmd_meeting_today)
    ml = meeting_subs.add_parser("list", parents=[_common])
    ml.set_defaults(func=functools.partial(cmd_entity_list, et=EntityType.MEETING))

    # review
    review_p = subparsers.add_parser("review", parents=[_common])
    review_subs = review_p.add_subparsers(dest="subcommand", required=True)
    rm = review_subs.add_parser("morning", parents=[_common])
    rm.set_defaults(func=cmd_review_morning)
    for kind in ("weekly", "monthly", "quarterly"):
        rp = review_subs.add_parser(kind, parents=[_common])
        rp.set_defaults(func=functools.partial(cmd_review_period, kind=kind))

    # search
    search_p = subparsers.add_parser("search", parents=[_common])
    search_p.add_argument("query")
    search_p.add_argument("--project", action="store_true")
    search_p.add_argument("--cookbook", action="store_true")
    search_p.add_argument("--knowledge", action="store_true")
    search_p.add_argument("--decision", action="store_true")
    search_p.add_argument("--resource", action="store_true")
    search_p.add_argument("--person", action="store_true")
    search_p.set_defaults(func=cmd_search)

    # sync
    sync_p = subparsers.add_parser("sync", parents=[_common])
    sync_p.set_defaults(func=cmd_sync)

    # plugin
    plugin_p = subparsers.add_parser("plugin", parents=[_common])
    plugin_subs = plugin_p.add_subparsers(dest="subcommand", required=True)
    pl = plugin_subs.add_parser("list", parents=[_common])
    pl.set_defaults(func=cmd_plugin_list)
    pi = plugin_subs.add_parser("install", parents=[_common])
    pi.add_argument("name")
    pi.add_argument("--source")
    pi.set_defaults(func=cmd_plugin_install)
    pr = plugin_subs.add_parser("remove", parents=[_common])
    pr.add_argument("name")
    pr.set_defaults(func=cmd_plugin_remove)
    pu = plugin_subs.add_parser("update", parents=[_common])
    pu.add_argument("name", nargs="?")
    pu.set_defaults(func=cmd_plugin_update)

    # index
    index_p = subparsers.add_parser("index", parents=[_common])
    index_subs = index_p.add_subparsers(dest="subcommand", required=True)
    ib = index_subs.add_parser("build", parents=[_common])
    ib.set_defaults(func=cmd_index_build)
    iu = index_subs.add_parser("update", parents=[_common])
    iu.set_defaults(func=cmd_index_update)
    ic = index_subs.add_parser("clean", parents=[_common])
    ic.set_defaults(func=cmd_index_clean)

    # completion
    comp_p = subparsers.add_parser("completion", parents=[_common])
    comp_p.add_argument("--shell", default="bash", choices=["bash", "zsh"])
    comp_p.set_defaults(func=cmd_completion)

    # validate (hidden, exposed via doctor-like check but also directly)
    validate_p = subparsers.add_parser("validate", parents=[_common])
    validate_p.set_defaults(func=cmd_validate)

    return parser


_common: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)


def _version() -> str:
    from kisuke import __version__

    return __version__


# ---------------------------------------------------------------------------
# Meeting handlers (defined late to keep grouping tidy)
# ---------------------------------------------------------------------------
def cmd_meeting_today(args: argparse.Namespace, ctx: CliContext) -> Result:
    from datetime import UTC, datetime

    today = datetime.now(UTC).date().isoformat()
    meetings = EntityService(ctx.repo()).list(EntityType.MEETING)
    today_meetings = [m for m in meetings if getattr(m, "date", "") == today]
    if not today_meetings:
        return Result("No meetings scheduled today.", {"date": today, "meetings": []})
    lines = [f"Meetings today ({today}):"]
    payload = []
    for meeting in today_meetings:
        lines.append(f"  {meeting.id}  {meeting.title}")
        payload.append(entity_to_dict(meeting))
    return Result("\n".join(lines), {"date": today, "meetings": payload})


def build_context(args: argparse.Namespace) -> CliContext:
    config = resolve_config()
    repo_root = resolve_repo_root()
    return CliContext(
        repo_root=repo_root,
        config=config,
        db_path=config.index_dir / "search.db",
        settings_path=config.data_dir / "settings.json",
        registry_path=config.data_dir / "plugins.json",
        last_focus_path=config.cache_dir / "last_resume.json",
        as_json=bool(getattr(args, "json", False)),
        quiet=bool(getattr(args, "quiet", False)),
        verbose=bool(getattr(args, "verbose", False)),
    )
