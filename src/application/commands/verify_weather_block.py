# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-081: Command contracts are defined before orchestration logic.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class RequestContext:
    actor_id: str
    roles: tuple[str, ...]
    correlation_id: str


@dataclass(frozen=True, slots=True)
class VerifyWeatherBlockCommand:
    weather_block_id: str
    approved: bool
    note: str | None = None
    idempotency_key: str | None = None


@dataclass(frozen=True, slots=True)
class VerifyWeatherBlockResult:
    weather_block_id: str
    status: str
    correlation_id: str


class WeatherBlockServicePort(Protocol):
    def verify_block(
        self,
        *,
        weather_block_id: str,
        approved: bool,
        reviewer_id: str,
        note: str | None,
        correlation_id: str,
    ) -> dict[str, Any]: ...


class AuditLogPort(Protocol):
    def log(self, *, action: str, correlation_id: str, actor_id: str, payload: dict[str, Any]) -> None: ...


class IdempotencyPort(Protocol):
    def get(self, *, key: str) -> dict[str, Any] | None: ...

    def set(self, *, key: str, value: dict[str, Any]) -> None: ...


class VerifyWeatherBlockDeps(Protocol):
    weather_block_service: WeatherBlockServicePort
    audit_log: AuditLogPort
    idempotency: IdempotencyPort | None


def handle(
    command: VerifyWeatherBlockCommand, *, ctx: RequestContext, deps: VerifyWeatherBlockDeps
) -> VerifyWeatherBlockResult:
    if not {"admin", "ops", "dispatcher"}.intersection(ctx.roles):
        raise PermissionError("forbidden")

    if command.idempotency_key and deps.idempotency is not None:
        cached = deps.idempotency.get(key=command.idempotency_key)
        if cached is not None:
            return VerifyWeatherBlockResult(
                weather_block_id=str(cached["weather_block_id"]),
                status=str(cached["status"]),
                correlation_id=ctx.correlation_id,
            )

    verified = deps.weather_block_service.verify_block(
        weather_block_id=command.weather_block_id,
        approved=command.approved,
        reviewer_id=ctx.actor_id,
        note=command.note,
        correlation_id=ctx.correlation_id,
    )

    status = str(verified.get("status", "verified" if command.approved else "rejected"))

    deps.audit_log.log(
        action="verify_weather_block",
        correlation_id=ctx.correlation_id,
        actor_id=ctx.actor_id,
        payload={"weather_block_id": command.weather_block_id, "approved": command.approved, "error_code": None},
    )

    if command.idempotency_key and deps.idempotency is not None:
        deps.idempotency.set(
            key=command.idempotency_key, value={"weather_block_id": command.weather_block_id, "status": status}
        )

    return VerifyWeatherBlockResult(
        weather_block_id=command.weather_block_id,
        status=status,
        correlation_id=ctx.correlation_id,
    )
