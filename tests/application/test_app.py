"""Application-layer unit tests.

These exercise the use-case services the CLI delegates to, without going through
argparse.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kisuke.application.config_app import ConfigService, resolve_config
from kisuke.application.entities import EntityService, build_entity, entity_to_dict
from kisuke.application.plugins import PluginService
from kisuke.application.tasks import TaskService
from kisuke.application.workspace import init_repository, repository_status, resolve_repo_root
from kisuke.domain.entities import Project
from kisuke.domain.lifecycle import EntityType, MissionStatus, ProjectStatus, TaskStatus
from kisuke.domain.owner import Owner
from kisuke.infrastructure.storage.repository import FileRepository


def _params(**kw: object) -> dict[str, object]:
    return kw


def test_build_entity_owners() -> None:
    mission = build_entity(EntityType.MISSION, _params(title="M"))
    assert mission.owner == Owner.kisuke_core()
    assert mission.status == MissionStatus.ACTIVE

    project = build_entity(EntityType.PROJECT, _params(title="P", mission=str(mission.id)))
    assert project.owner.entity_id == mission.id
    assert project.status == ProjectStatus.ACTIVE

    task = build_entity(EntityType.TASK, _params(title="T", project=str(project.id)))
    assert task.owner.entity_id == project.id
    assert task.status == TaskStatus.TODO

    cookbook = build_entity(EntityType.COOKBOOK, _params(title="C"))
    assert cookbook.owner == Owner.kisuke_core()

    person = build_entity(EntityType.PERSON, _params(title="Pe"))
    assert person.owner == Owner.independent()


def test_build_entity_requires_parent() -> None:
    with pytest.raises(ValueError, match="requires --mission"):
        build_entity(EntityType.PROJECT, _params(title="P"))


def test_entity_to_dict_serializes() -> None:
    mission = build_entity(EntityType.MISSION, _params(title="M", tags=["a", "b"]))
    data = entity_to_dict(mission)
    assert data["title"] == "M"
    assert data["owner"] == "kisuke-core"
    assert data["tags"] == ["a", "b"]
    assert data["type"] == "mission"
    assert isinstance(data["created_at"], str)


def test_entity_service_crud(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    service = EntityService(repo)
    mission = service.create(EntityType.MISSION, _params(title="M"))
    assert len(service.list(EntityType.MISSION)) == 1
    loaded = service.show(EntityType.MISSION, mission.id)
    assert loaded.title == "M"
    path = service.path(EntityType.MISSION, mission.id)
    assert path.exists()
    archived = service.archive(EntityType.MISSION, mission.id)
    assert archived.status == MissionStatus.ARCHIVED


def test_task_service_next_done_move(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    mission = build_entity(EntityType.MISSION, _params(title="M"))
    repo.save(mission)
    p1 = build_entity(EntityType.PROJECT, _params(title="P1", mission=str(mission.id)))
    repo.save(p1)
    p2 = build_entity(EntityType.PROJECT, _params(title="P2", mission=str(mission.id)))
    repo.save(p2)

    tasks = TaskService(repo)
    task = tasks.add(_params(title="T", project=str(p1.id)))

    assert tasks.next(str(p1.id)).id == task.id
    tasks.move(task.id, str(p2.id))
    assert tasks.next(str(p2.id)).id == task.id
    tasks.done(task.id)
    assert tasks.next(str(p1.id)) is None
    assert tasks.next(str(p2.id)) is None
    reloaded_p1 = repo.load(EntityType.PROJECT, p1.id)
    assert isinstance(reloaded_p1, Project)
    assert task.id not in reloaded_p1.tasks


def test_plugin_service(tmp_path: Path) -> None:
    service = PluginService(tmp_path / "plugins.json")
    assert service.list_plugins() == []
    service.install("demo", "git")
    assert [p.name for p in service.list_plugins()] == ["demo"]
    assert service.remove("demo") is True
    assert service.list_plugins() == []
    with pytest.raises(ValueError, match="not installed"):
        service.update("missing")


def test_config_service(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    service = ConfigService(path)
    service.set("log_level", "DEBUG")
    assert service.get("log_level")["log_level"] == "DEBUG"
    with pytest.raises(ValueError, match="unknown config key"):
        service.set("bogus", "x")


def test_resolve_config_merges(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KISUKE_DATA_DIR", str(tmp_path / "data"))
    ConfigService(tmp_path / "data" / "settings.json").set("log_level", "INFO")
    config = resolve_config()
    assert config.log_level == 20  # logging.INFO


def test_workspace_init_and_status(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    created = init_repository(root)
    assert (root / "missions").is_dir()
    assert len(created) > 0
    status = repository_status(root)
    assert status["initialized"] is True
    assert isinstance(status["counts"], dict)


def test_resolve_repo_root_default(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("KISUKE_REPO_DIR", raising=False)
    monkeypatch.setenv("KISUKE_DATA_DIR", str(tmp_path / "data"))
    # Without KISUKE_REPO_DIR the root is cwd; just ensure it returns a Path.
    assert isinstance(resolve_repo_root(), Path)
