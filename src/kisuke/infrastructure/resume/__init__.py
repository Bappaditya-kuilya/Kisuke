"""Infrastructure resume package.

Pure Infrastructure layer: reconstructs working context from the Markdown
repository using only stored data. Reuses the Storage repository and the Search
API (via public interfaces); contains no AI, no network, and never writes.
"""

from __future__ import annotations

from .model import ResumeResult
from .ordering import order_entities
from .service import ResumeService

__all__ = ["ResumeResult", "order_entities", "ResumeService"]
