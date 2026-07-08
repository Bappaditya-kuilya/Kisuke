"""Provider registry.

Holds the set of available AI providers and selects one for use. Selection is
configuration-driven: a named provider is preferred, otherwise the first
*available* provider wins. The registry never imports or configures providers
itself beyond construction; availability is decided by each provider.
"""

from __future__ import annotations

from kisuke.ai.interfaces import AIProvider


class ProviderRegistry:
    """Registry of available AI providers."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        if not provider.name:
            raise ValueError("provider must declare a non-empty name")
        self._providers[provider.name] = provider

    def get(self, name: str) -> AIProvider | None:
        return self._providers.get(name)

    def all(self) -> list[AIProvider]:
        return list(self._providers.values())

    def available(self) -> list[AIProvider]:
        """Providers that report themselves available in this environment."""
        return [p for p in self._providers.values() if p.is_available()]

    def select(self, name: str | None = None) -> AIProvider | None:
        """Select a provider by name, or the first available one.

        If ``name`` is given but unavailable, selection falls back to the first
        available provider so core workflows degrade gracefully. An unknown
        name returns ``None`` to surface configuration errors.
        """
        if name is not None:
            named = self._providers.get(name)
            if named is not None and named.is_available():
                return named
            # Known but unavailable: fall back.
            if named is not None:
                available = self.available()
                return available[0] if available else None
            # Unknown name: return None to surface misconfiguration.
            return None
        available = self.available()
        return available[0] if available else None
