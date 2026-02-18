# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Contract-first schema validation is enforced before orchestration.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


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
        _ = correlation_id
        schema = self._registry.get_schema(schema_id)
        try:
            import jsonschema  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("jsonschema dependency is required for KR-081 validation") from exc

        try:
            jsonschema.validate(instance=payload, schema=schema)
            return ValidationResult(ok=True, schema_id=schema_id)
        except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
            error = ContractValidationError(
                "Contract validation failed",
                schema_id=schema_id,
                details={"message": str(exc), "path": list(exc.path), "schema_path": list(exc.schema_path)},
            )
            return ValidationResult(ok=False, schema_id=schema_id, error=error)
