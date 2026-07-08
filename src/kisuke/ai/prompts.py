"""Prompt abstraction.

Prompts are version-controlled, reusable, and provider-independent. They are
never embedded inside application logic: the service renders a named prompt with
the packaged context. Templates use ``str.format`` substitution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Prompt:
    """A versioned, reusable prompt template."""

    id: str
    version: str
    template: str
    description: str = ""

    def render(self, **kwargs: Any) -> str:
        """Render the template, raising ``KeyError`` on missing placeholders."""
        return self.template.format(**kwargs)


class PromptLibrary:
    """Registry of built-in prompts."""

    def __init__(self) -> None:
        self._prompts: dict[str, Prompt] = {}
        self._register_builtins()

    def register(self, prompt: Prompt) -> None:
        self._prompts[prompt.id] = prompt

    def get(self, prompt_id: str) -> Prompt:
        if prompt_id not in self._prompts:
            raise KeyError(f"unknown prompt: {prompt_id}")
        return self._prompts[prompt_id]

    def ids(self) -> list[str]:
        return sorted(self._prompts)

    def _register_builtins(self) -> None:
        self.register(
            Prompt(
                "system",
                "1.0",
                "You are Kisuke Assistant, a local-first, offline-friendly aid. "
                "Answer using only the context provided. Never invent facts.",
            )
        )
        self.register(
            Prompt(
                "summarize",
                "1.0",
                "Summarize the following Kisuke working context concisely.\n\n"
                "Context:\n{context}",
                description="Summarize the current working context.",
            )
        )
        self.register(
            Prompt(
                "explain",
                "1.0",
                "Explain the current task in the given context.\n\n"
                "Context:\n{context}\n\nQuestion: {question}",
                description="Explain a task or entity given context.",
            )
        )
        self.register(
            Prompt(
                "next_action",
                "1.0",
                "Given the context, suggest the single next concrete action.\n\n"
                "Context:\n{context}",
                description="Suggest the next action.",
            )
        )
        self.register(
            Prompt(
                "classify",
                "1.0",
                "Classify the priority of the following context. "
                'Respond ONLY with JSON: {{"priority": "high|medium|low"}}.\n\n'
                "Context:\n{context}",
                description="Classify context priority (structured JSON).",
            )
        )
        self.register(
            Prompt(
                "extract_keywords",
                "1.0",
                "Extract up to 5 search keywords from the context. "
                'Respond ONLY with JSON: {{"keywords": ["a", "b", "c"]}}.\n\n'
                "Context:\n{context}",
                description="Extract search keywords (structured JSON).",
            )
        )
