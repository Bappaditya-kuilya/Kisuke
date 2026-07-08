"""Task application service.

Task-specific orchestration that the generic :class:`EntityService` does not
cover: selecting the next action, completing a task, and moving a task between
projects while keeping both ends consistent.
"""

from __future__ import annotations

from dataclasses import replace

from kisuke.domain.entities import Project, Task
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import EntityType, ProjectStatus, TaskStatus
from kisuke.domain.owner import Owner
from kisuke.domain.timestamp import Timestamp
from kisuke.infrastructure.storage.repository import FileRepository


class TaskService:
    """Operations on Task entities beyond simple CRUD."""

    def __init__(self, repo: FileRepository) -> None:
        self.repo = repo

    def add(self, params: dict[str, object]) -> Task:
        from kisuke.application.entities import EntityService

        entity = EntityService(self.repo).create(EntityType.TASK, params)
        assert isinstance(entity, Task)
        return entity

    def list(self, project: str | None = None, status: str | None = None) -> list[Task]:
        tasks = [t for t in self.repo.all(EntityType.TASK) if isinstance(t, Task)]
        if project is not None:
            pid = EntityId.from_string(project)
            tasks = [t for t in tasks if t.owner.entity_id == pid]
        if status is not None:
            tasks = [t for t in tasks if str(t.status) == status]
        return tasks

    def _focus_project(self) -> Project | None:
        projects = [p for p in self.repo.all(EntityType.PROJECT) if isinstance(p, Project)]
        if not projects:
            return None
        active = [p for p in projects if p.status == ProjectStatus.ACTIVE]
        chosen = active[0] if active else projects[0]
        return chosen

    def next(self, project: str | None = None) -> Task | None:
        if project is not None:
            loaded = self.repo.load(EntityType.PROJECT, EntityId.from_string(project))
            assert isinstance(loaded, Project)
            focus: Project | None = loaded
        else:
            focus = self._focus_project()
        if focus is None:
            return None
        if focus.next_action is not None and self.repo.exists(EntityType.TASK, focus.next_action):
            task = self.repo.load(EntityType.TASK, focus.next_action)
            if isinstance(task, Task):
                return task
        candidates = [
            t
            for tid in focus.tasks
            if self.repo.exists(EntityType.TASK, tid)
            and isinstance((t := self.repo.load(EntityType.TASK, tid)), Task)
        ]
        candidates.sort(key=lambda t: str(t.id))
        non_done = [task for task in candidates if task.status != TaskStatus.DONE]
        return non_done[0] if non_done else None

    def done(self, entity_id: EntityId) -> Task:
        task = self.repo.load(EntityType.TASK, entity_id)
        assert isinstance(task, Task)
        updated = replace(task, status=TaskStatus.DONE, updated_at=Timestamp.now())
        self.repo.save(updated)
        return updated

    def move(self, entity_id: EntityId, target_project: str) -> Task:
        task = self.repo.load(EntityType.TASK, entity_id)
        assert isinstance(task, Task)
        new_pid = EntityId.from_string(target_project)
        old_pid = task.owner.entity_id
        updated = replace(task, owner=Owner.of(new_pid), updated_at=Timestamp.now())
        self.repo.save(updated)
        if (
            old_pid is not None
            and old_pid != new_pid
            and self.repo.exists(EntityType.PROJECT, old_pid)
        ):
            old = self.repo.load(EntityType.PROJECT, old_pid)
            assert isinstance(old, Project)
            self.repo.save(
                replace(
                    old, tasks=[t for t in old.tasks if t != entity_id], updated_at=Timestamp.now()
                )
            )
        new = self.repo.load(EntityType.PROJECT, new_pid)
        assert isinstance(new, Project)
        if entity_id not in new.tasks:
            self.repo.save(replace(new, tasks=new.tasks + [entity_id], updated_at=Timestamp.now()))
        return updated
