"""Repository validator.

Scans the repository, parses every entity file incrementally, validates the
raw frontmatter (schema + lifecycle), then validates the fully-parsed entity
collection (ownership, relationships, duplicate IDs). Produces a deterministic
ValidationReport. The validator only reads the repository; it never modifies it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kisuke.domain.entities import Entity
from kisuke.domain.ids import EntityId
from kisuke.domain.lifecycle import STATUS_ENUMS, EntityType
from kisuke.domain.relationships import (
    NEXT_ACTION_OWNER,
    OWNERSHIP_RULES,
    RELATIONSHIP_FIELDS,
)
from kisuke.infrastructure.validation.parser import IncrementalParser, ParseResult
from kisuke.infrastructure.validation.report import (
    IssueCode,
    IssueSeverity,
    ValidationIssue,
    ValidationReport,
)
from kisuke.infrastructure.validation.scanner import RepositoryScanner
from kisuke.infrastructure.validation.schema import (
    safe_entity_id,
    safe_entity_type,
    schema_issues,
)


class RepositoryValidator:
    """Validates an entire Markdown repository."""

    def __init__(
        self,
        root: Path,
        scanner: RepositoryScanner | None = None,
        parser: IncrementalParser | None = None,
    ) -> None:
        self.root = Path(root)
        self.scanner = scanner or RepositoryScanner(self.root)
        self.parser = parser or IncrementalParser()

    def validate(self) -> ValidationReport:
        issues: list[ValidationIssue] = []
        entities: list[Entity] = []

        for path in self.scanner.discover():
            result = self.parser.parse_file(path)
            issues.extend(self._validate_file(result))
            if result.entity is not None and result.error is None:
                entities.append(result.entity)

        issues.extend(self._validate_collection(entities))
        return ValidationReport(root=self.root, issues=issues)

    def _validate_file(self, result: ParseResult) -> list[ValidationIssue]:
        fm = result.fm
        if fm is None:
            return [
                ValidationIssue(
                    IssueCode.PARSE_ERROR, IssueSeverity.ERROR, None, None, result.error or ""
                )
            ]

        et = safe_entity_type(fm.get("type"))
        eid = safe_entity_id(fm.get("id"))

        # Frontmatter is readable: validate its shape before constructing.
        issues = schema_issues(fm, et)
        if issues:
            return issues
        issues.extend(self._lifecycle_issues(fm, et, eid))
        if issues:
            return issues

        # Frontmatter is well-formed; the entity must be constructible.
        if result.entity is None:
            return [
                ValidationIssue(
                    IssueCode.PARSE_ERROR, IssueSeverity.ERROR, et, eid,
                    result.error or "entity construction failed",
                )
            ]
        return []

    @staticmethod
    def _lifecycle_issues(
        fm: dict[str, Any], et: EntityType | None, eid: str | None
    ) -> list[ValidationIssue]:
        status = fm.get("status")
        if status is None or et is None:
            return []
        enum_cls = STATUS_ENUMS.get(et)
        if enum_cls is None:
            return []
        try:
            enum_cls(status)
        except ValueError:
            return [
                ValidationIssue(
                    IssueCode.LIFECYCLE, IssueSeverity.ERROR, et, eid,
                    f"{et} has no status {status!r}",
                )
            ]
        return []

    def _validate_collection(self, entities: list[Entity]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        by_id: dict[EntityId, Entity] = {}

        for entity in entities:
            if entity.id in by_id:
                issues.append(
                    ValidationIssue(
                        IssueCode.DUPLICATE_ID, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"Duplicate entity ID: {entity.id}",
                    )
                )
            else:
                by_id[entity.id] = entity

        for entity in entities:
            issues.extend(self._check_ownership(entity, by_id))
            issues.extend(self._check_relationships(entity, by_id))
        return issues

    @staticmethod
    def _check_ownership(
        entity: Entity, by_id: dict[EntityId, Entity]
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        rule = OWNERSHIP_RULES[entity.entity_type]

        if rule.sentinel is not None:
            if entity.owner.sentinel != rule.sentinel:
                issues.append(
                    ValidationIssue(
                        IssueCode.OWNERSHIP, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} must be owned by sentinel "
                        f"{rule.sentinel!r}, got {entity.owner!r}",
                    )
                )
        elif rule.owner_type is not None or rule.parent:
            if entity.owner.entity_id is None:
                issues.append(
                    ValidationIssue(
                        IssueCode.OWNERSHIP, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} must be owned by an entity, "
                        f"got sentinel {entity.owner.sentinel!r}",
                    )
                )

        owner_id = entity.owner.entity_id
        if owner_id is not None:
            owner_entity = by_id.get(owner_id)
            if owner_entity is None:
                issues.append(
                    ValidationIssue(
                        IssueCode.OWNERSHIP, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} references missing owner {owner_id}",
                    )
                )
            elif rule.owner_type is not None and owner_entity.entity_type != rule.owner_type:
                issues.append(
                    ValidationIssue(
                        IssueCode.OWNERSHIP, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} owned by "
                        f"{owner_entity.entity_type} but expected {rule.owner_type}",
                    )
                )
        return issues

    @staticmethod
    def _check_relationships(
        entity: Entity, by_id: dict[EntityId, Entity]
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        typed = RELATIONSHIP_FIELDS.get(entity.entity_type, {})

        for field_name, allowed in typed.items():
            seen: set[EntityId] = set()
            for ref in getattr(entity, field_name):
                if ref in seen:
                    issues.append(
                        ValidationIssue(
                            IssueCode.INVALID_REFERENCE, IssueSeverity.ERROR,
                            entity.entity_type, str(entity.id),
                            f"Duplicate reference {ref} in {entity.entity_type} {entity.id}",
                        )
                    )
                    continue
                seen.add(ref)
                target = by_id.get(ref)
                if target is None:
                    issues.append(
                        ValidationIssue(
                            IssueCode.ORPHAN_REFERENCE, IssueSeverity.ERROR,
                            entity.entity_type, str(entity.id),
                            f"{entity.entity_type} {entity.id} references missing entity {ref}",
                        )
                    )
                elif target.entity_type not in allowed:
                    issues.append(
                        ValidationIssue(
                            IssueCode.INVALID_REFERENCE, IssueSeverity.ERROR,
                            entity.entity_type, str(entity.id),
                            f"{entity.entity_type} {entity.id} references disallowed type "
                            f"{target.entity_type} via {ref}",
                        )
                    )

        seen = set()
        for ref in entity.references:
            if ref in seen:
                continue
            seen.add(ref)
            if by_id.get(ref) is None:
                issues.append(
                    ValidationIssue(
                        IssueCode.ORPHAN_REFERENCE, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} references missing entity {ref}",
                    )
                )

        for ref in entity.attachments:
            target = by_id.get(ref)
            if target is None:
                issues.append(
                    ValidationIssue(
                        IssueCode.ORPHAN_REFERENCE, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} references missing attachment {ref}",
                    )
                )
            elif target.entity_type != EntityType.ATTACHMENT:
                issues.append(
                    ValidationIssue(
                        IssueCode.INVALID_REFERENCE, IssueSeverity.ERROR,
                        entity.entity_type, str(entity.id),
                        f"{entity.entity_type} {entity.id} attachment {ref} is not an Attachment",
                    )
                )

        next_type = NEXT_ACTION_OWNER.get(entity.entity_type)
        if next_type is not None:
            next_action = getattr(entity, "next_action", None)
            if next_action is not None:
                target = by_id.get(next_action)
                if target is None:
                    issues.append(
                        ValidationIssue(
                            IssueCode.ORPHAN_REFERENCE, IssueSeverity.ERROR,
                            entity.entity_type, str(entity.id),
                            f"{entity.entity_type} {entity.id} next action references "
                            f"missing entity {next_action}",
                        )
                    )
                elif target.entity_type != next_type:
                    issues.append(
                        ValidationIssue(
                            IssueCode.INVALID_REFERENCE, IssueSeverity.ERROR,
                            entity.entity_type, str(entity.id),
                            f"{entity.entity_type} {entity.id} next action {next_action} "
                            f"is not a {next_type}",
                        )
                    )
        return issues
