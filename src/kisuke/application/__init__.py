"""Application layer for Kisuke.

Use-case orchestration that sits between the CLI (adapter) and the Domain /
Infrastructure layers. Services here coordinate repositories, search, resume,
and validation; they contain no business rules of their own beyond the wiring
required to construct valid commands.
"""

from __future__ import annotations

from kisuke.application.config_app import ConfigService, default_settings_path, resolve_config
from kisuke.application.doctor import Check, DoctorService
from kisuke.application.entities import EntityService, build_entity, entity_to_dict
from kisuke.application.index_app import IndexService
from kisuke.application.plugins import Plugin, PluginService
from kisuke.application.resume_app import ResumeApp
from kisuke.application.search_app import SearchService
from kisuke.application.tasks import TaskService
from kisuke.application.validation_app import ValidateService
from kisuke.application.workspace import (
    init_repository,
    repository_status,
    resolve_repo_root,
)

__all__ = [
    "Check",
    "ConfigService",
    "DoctorService",
    "EntityService",
    "IndexService",
    "Plugin",
    "PluginService",
    "ResumeApp",
    "SearchService",
    "TaskService",
    "ValidateService",
    "build_entity",
    "default_settings_path",
    "entity_to_dict",
    "init_repository",
    "repository_status",
    "resolve_config",
    "resolve_repo_root",
]
