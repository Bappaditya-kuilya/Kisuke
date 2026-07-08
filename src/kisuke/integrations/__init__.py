"""Integrations package for Kisuke.

Adapters to external systems (Git, filesystem, Markdown, export, sync). Every
integration is optional, pluggable, and never owns canonical data. The package
exposes discovery helpers that build a configured :class:`PluginRegistry`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kisuke.integrations.base import BaseIntegration
from kisuke.integrations.change import FileChange, RepoSnapshot, detect_changes, snapshot, summarize
from kisuke.integrations.config import IntegrationConfig, IntegrationConfigEntry
from kisuke.integrations.export import Exporter, ExportResult
from kisuke.integrations.git import GitIntegration
from kisuke.integrations.markdown_import import ImportResult, MarkdownImporter
from kisuke.integrations.sync import SyncResult, SyncService
from kisuke.integrations.watcher import FileSystemWatcher
from kisuke.plugins.interfaces import Integration, IntegrationInfo
from kisuke.plugins.registry import PluginRegistry


def builtin_integrations(root: Path, options: dict[str, Any] | None = None) -> list[Integration]:
    """Return the built-in integration instances for a repository root."""
    opts = options or {}
    return [
        GitIntegration(root, opts.get("git")),
    ]


def build_registry(
    root: Path,
    config_path: Path,
    plugins_dir: Path | None = None,
    options: dict[str, Any] | None = None,
) -> PluginRegistry:
    """Construct a registry, register built-in integrations, and discover plugins."""
    registry = PluginRegistry(config_path)
    for integration in builtin_integrations(root, options):
        integration.configure(options or {})
        registry.register(integration)
    registry.discover(plugins_dir)
    return registry


__all__ = [
    "BaseIntegration",
    "ExportResult",
    "Exporter",
    "FileChange",
    "FileSystemWatcher",
    "GitIntegration",
    "ImportResult",
    "Integration",
    "IntegrationConfig",
    "IntegrationConfigEntry",
    "IntegrationInfo",
    "MarkdownImporter",
    "PluginRegistry",
    "RepoSnapshot",
    "SyncResult",
    "SyncService",
    "builtin_integrations",
    "build_registry",
    "detect_changes",
    "snapshot",
    "summarize",
]
