# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Contract-first schema validation is enforced in application layer.

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class SchemaRegistry(Protocol):
    def get_schema(self, schema_id: str) -> dict[str, Any]: ...


class ContractValidationError(ValueError):
    def __init__(self, message: str, *, schema_id: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.schema_id = schema_id
        self.details = details or {}


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    schema_id: str
    error: ContractValidationError | None = None


class ContractValidatorService:
    def __init__(self, registry: SchemaRegistry) -> None:
        self._registry = registry

    def validate(self, *, schema_id: str, payload: Any, correlation_id: str) -> ValidationResult:
        schema = self._registry.get_schema(schema_id)
        try:
            import jsonschema  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("jsonschema dependency is required for KR-081 validation") from exc

        try:
            jsonschema.validate(instance=payload, schema=schema)
            logger.info("contract_validate_ok schema_id=%s correlation_id=%s", schema_id, correlation_id)
            return ValidationResult(ok=True, schema_id=schema_id)
        except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
            err = ContractValidationError(
                "Contract validation failed",
                schema_id=schema_id,
                details={"message": str(exc), "path": list(exc.path), "schema_path": list(exc.schema_path)},
            )
            logger.warning(
                "contract_validate_fail schema_id=%s correlation_id=%s details=%s",
                schema_id,
                correlation_id,
                json.dumps(err.details, ensure_ascii=False),
            )
            return ValidationResult(ok=False, schema_id=schema_id, error=err)
