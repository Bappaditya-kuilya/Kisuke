"""Plugin package for Kisuke.

Holds the plugin/integration interface and registry. Integrations live under
``kisuke.integrations`` and register themselves with this registry.
"""

from __future__ import annotations

from kisuke.plugins.interfaces import Integration, IntegrationInfo
from kisuke.plugins.registry import PluginRegistry

__all__ = ["Integration", "IntegrationInfo", "PluginRegistry"]
