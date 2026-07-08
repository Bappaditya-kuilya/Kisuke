"""Resume service.

Reconstructs the current working context from the Markdown repository using
only stored data (no inference, no AI, no network). The focus Mission/Project
are selected deterministically; related entities are gathered by one-hop graph
traversal from the focus project and mission.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypeVar, cast

from kisuke.domain.entities import (
    Decision,
    Entity,
    Knowledge,
    Meeting,
    Mission,
    Person,
    Project,
    Resource,
    Review,
    Task,
)
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import EntityType, MissionStatus, ProjectStatus
from kisuke.infrastructure.resume.model import ResumeResult
from kisuke.infrastructure.resume.ordering import order_entities
from kisuke.infrastructure.search.api import SearchEngine
from kisuke.infrastructure.storage.repository import FileRepository

T = TypeVar("T", bound=Entity)


class ResumeService:
    """Reconstructs working context from the repository."""

    def __init__(self, root: str | Path, search: SearchEngine | None = None) -> None:
        self.root = Path(root)
        self.repo = FileRepository(self.root)
        self.search = search

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def resume(
        self,
        focus_mission: str | EntityId | None = None,
        focus_project: str | EntityId | None = None,
    ) -> ResumeResult:
        mission_id = (
            EntityId.from_string(focus_mission) if isinstance(focus_mission, str) else focus_mission
        )
        project_id = (
            EntityId.from_string(focus_project) if isinstance(focus_project, str) else focus_project
        )
        entities = self._load_all()
        mission = self._select_mission(entities, mission_id)
        project = self._select_project(entities, mission, project_id)
        return self._build(entities, mission, project)

    def resume_from_search(self, query: str) -> ResumeResult | None:
        if self.search is None:
            raise RuntimeError("ResumeService was not configured with a SearchEngine")
        hits = self.search.search(query, type="project")
        if not hits:
            return None
        return self.resume(focus_project=EntityId.from_string(hits[0].entity_id))

    def validate(self, result: ResumeResult) -> list[str]:
        problems: list[str] = []
        if result.mission is not None and result.project is not None:
            owner_id = result.project.owner.entity_id
            if owner_id is None or owner_id != result.mission.id:
                problems.append("Project is not owned by the focus Mission")
        if result.next_action is not None:
            task_ids = {t.id for t in result.related_tasks}
            if result.next_action.id not in task_ids:
                problems.append("Next Action is not among the project's related tasks")
        return problems

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _load_all(self) -> dict[EntityId, Entity]:
        out: dict[EntityId, Entity] = {}
        for entity_type in EntityType:
            for entity in self.repo.all(entity_type):
                out[entity.id] = entity
        return out

    def _select_mission(
        self, entities: dict[EntityId, Entity], override: EntityId | None
    ) -> Mission | None:
        missions = [e for e in entities.values() if e.entity_type == EntityType.MISSION]
        missions.sort(key=lambda m: str(m.id))
        if override is not None and override in entities:
            candidate = entities[override]
            if isinstance(candidate, Mission):
                return candidate
        active = [m for m in missions if m.status == MissionStatus.ACTIVE]
        if active:
            return cast(Mission, active[0])
        return cast(Mission, missions[0]) if missions else None

    def _select_project(
        self,
        entities: dict[EntityId, Entity],
        mission: Mission | None,
        override: EntityId | None,
    ) -> Project | None:
        projects = [e for e in entities.values() if e.entity_type == EntityType.PROJECT]
        if mission is not None:
            projects = [p for p in projects if p.owner.entity_id == mission.id]
        projects.sort(key=lambda p: str(p.id))
        if override is not None and override in entities:
            candidate = entities[override]
            if isinstance(candidate, Project):
                return candidate
        active = [p for p in projects if p.status == ProjectStatus.ACTIVE]
        if active:
            return cast(Project, active[0])
        return cast(Project, projects[0]) if projects else None

    def _build(
        self,
        entities: dict[EntityId, Entity],
        mission: Mission | None,
        project: Project | None,
    ) -> ResumeResult:
        task_ids: set[EntityId] = set(project.tasks) if project else set()
        knowledge_ids: set[EntityId] = set(project.knowledge) if project else set()
        decision_ids: set[EntityId] = set(project.decisions) if project else set()
        meeting_ids: set[EntityId] = set(project.meetings) if project else set()
        resource_ids: set[EntityId] = set(project.resources) if project else set()
        people_ids: set[EntityId] = set(project.people) if project else set()
        review_ids: set[EntityId] = set(mission.reviews) if mission else set()

        # Meetings that reference the focus project (relationship direction).
        if project is not None:
            for entity in entities.values():
                if isinstance(entity, Meeting) and project.id in entity.projects:
                    meeting_ids.add(entity.id)

        # Resources referenced by knowledge and tasks.
        for kid in knowledge_ids:
            knowledge_entity = entities.get(kid)
            if isinstance(knowledge_entity, Knowledge):
                resource_ids.update(knowledge_entity.resources)
        for tid in task_ids:
            task = entities.get(tid)
            if isinstance(task, Task):
                resource_ids.update(
                    r for r in task.references if _is_type(entities, r, EntityType.RESOURCE)
                )
        for did in decision_ids:
            decision = entities.get(did)
            if isinstance(decision, Decision):
                resource_ids.update(
                    r for r in decision.references if _is_type(entities, r, EntityType.RESOURCE)
                )

        # People attending the related meetings.
        for mid in meeting_ids:
            meeting = entities.get(mid)
            if isinstance(meeting, Meeting):
                people_ids.update(meeting.people)

        related_tasks = self._collect(entities, task_ids, Task)
        knowledge = self._collect(entities, knowledge_ids, Knowledge)
        decisions = self._collect(entities, decision_ids, Decision)
        meetings = self._collect(entities, meeting_ids, Meeting)
        resources = self._collect(entities, resource_ids, Resource)
        people = self._collect(entities, people_ids, Person)
        reviews = self._collect(entities, review_ids, Review)

        next_action: Task | None = None
        if project is not None and project.next_action is not None:
            candidate = entities.get(project.next_action)
            if isinstance(candidate, Task):
                next_action = candidate

        return ResumeResult(
            mission=mission,
            project=project,
            next_action=next_action,
            related_tasks=related_tasks,
            knowledge=knowledge,
            decisions=decisions,
            meetings=meetings,
            resources=resources,
            people=people,
            reviews=reviews,
        )

    def _collect(
        self, entities: dict[EntityId, Entity], ids: set[EntityId], cls: type[T]
    ) -> list[T]:
        found = [e for eid in ids if (e := entities.get(eid)) is not None and isinstance(e, cls)]
        return cast(list[T], order_entities(found))


def _is_type(entities: dict[EntityId, Entity], ref: EntityId, et: EntityType) -> bool:
    entity = entities.get(ref)
    return entity is not None and entity.entity_type == et
