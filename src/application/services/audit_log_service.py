# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-033: Audit actions are emitted and persisted by a single application service.

from __future__ import annotations

import enum
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Protocol


class AuditAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    ASSIGN = "assign"
    SCHEDULE = "schedule"
    START = "start"
    COMPLETE = "complete"
    EXPORT = "export"


@dataclass(frozen=True, slots=True)
class Actor:
    actor_id: str
    roles: tuple[str, ...] = ()
    tenant_id: str | None = None


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    ts_ms: int
    correlation_id: str
    actor: Actor
    action: AuditAction
    resource_type: str
    resource_id: str
    outcome: str
    meta: dict[str, Any] = field(default_factory=dict)


class AuditLogRepository(Protocol):
    def append(self, event: AuditEvent) -> None: ...


class Clock(Protocol):
    def now_ms(self) -> int: ...


class SystemClock:
    def now_ms(self) -> int:
        return int(time.time() * 1000)


class AuditLogService:
    def __init__(self, repo: AuditLogRepository, clock: Clock | None = None) -> None:
        self._repo = repo
        self._clock = clock or SystemClock()

    def emit(
        self,
        *,
        correlation_id: str,
        actor: Actor,
        action: AuditAction,
        resource_type: str,
        resource_id: str,
        outcome: str,
        meta: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            ts_ms=self._clock.now_ms(),
            correlation_id=correlation_id,
            actor=actor,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            outcome=outcome,
            meta=meta or {},
        )
        self._repo.append(event)
        return event
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Audit olaylarını tek noktadan üretmek ve persistence'e append etmek.
Sorumluluk: Use-case orkestrasyonu; domain service + ports birleşimi; policy enforcement.
Girdi/Çıktı (Contract/DTO/Event): Girdi: API/Job/Worker tetiklemesi. Çıktı: DTO, event, state transition.
Güvenlik (RBAC/PII/Audit): RBAC burada; PII redaction; audit log; rate limit (gereken yerde).
Hata Modları (idempotency/retry/rate limit): 400/403/409/429/5xx mapping; retry-safe tasarım; idempotency key/hard gate’ler.
Observability (log fields/metrics/traces): correlation_id, latency, error_code; use-case metric sayaçları.
Testler: Unit + integration; kritik akış için e2e (özellikle ödeme/planlama/kalibrasyon).
Bağımlılıklar: Domain + ports + infra implementasyonları + event bus.
Notlar/SSOT: Contract-first (KR-081) ve kritik kapılar (KR-018/KR-033/KR-015) application katmanında enforce edilir.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol



class AuditLogPort(Protocol):
    def append(self, *, event_type: str, correlation_id: str, payload: dict[str, Any]) -> None: ...


@dataclass(frozen=True, slots=True)
class AuditEntry:
    event_type: str
    correlation_id: str
    payload: dict[str, Any]


@dataclass(slots=True)
class AuditLogService:
    audit_port: AuditLogPort

    def append(self, entry: AuditEntry) -> None:
        # KR-033: Record auditable action with correlation.
        # KR-033: kritik karar ve geçitlerde audit izi tek noktadan tutulur.
        self.audit_port.append(
            event_type=entry.event_type,
            correlation_id=entry.correlation_id,
            payload=entry.payload,
        )
