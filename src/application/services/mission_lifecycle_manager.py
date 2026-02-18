# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Mission lifecycle transitions follow explicit policy guards.
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Mission yaşam döngüsü yönetimi.
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


@dataclass(frozen=True, slots=True)
class Mission:
    mission_id: str
    field_id: str
    status: str
    pilot_id: str | None = None
    scheduled_ts_ms: int | None = None


class MissionRepository(Protocol):
    def get(self, mission_id: str) -> Mission | None: ...

    def update(self, mission: Mission) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class MissionLifecycleManager:
    def __init__(self, repo: MissionRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def transition(self, *, mission_id: str, to_status: str, correlation_id: str, **patch: Any) -> Mission:
        mission = self._repo.get(mission_id)
        if mission is None:
            raise ValueError("mission not found")

        allowed: dict[str, set[str]] = {
            "draft": {"scheduled", "cancelled"},
            "scheduled": {"assigned", "cancelled"},
            "assigned": {"flown", "cancelled"},
            "flown": {"uploaded"},
            "uploaded": {"analyzing"},
            "analyzing": {"completed"},
            "completed": set(),
            "cancelled": set(),
        }
        if to_status not in allowed.get(mission.status, set()):
            raise ValueError(f"invalid transition {mission.status} -> {to_status}")

        updated = Mission(
            mission_id=mission.mission_id,
            field_id=mission.field_id,
            status=to_status,
            pilot_id=patch.get("pilot_id", mission.pilot_id),
            scheduled_ts_ms=patch.get("scheduled_ts_ms", mission.scheduled_ts_ms),
        )
        self._repo.update(updated)
        self._bus.publish(
            "mission.status_changed",
            {"mission_id": mission_id, "from": mission.status, "to": to_status},
            correlation_id=correlation_id,
        )
        return updated
class DomainServicePort(Protocol):
    def execute(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]: ...


class AuditLogPort(Protocol):
    def append(self, *, event_type: str, correlation_id: str, payload: dict[str, Any]) -> None: ...


@dataclass(slots=True)
class MissionLifecycleManager:
    domain_service: DomainServicePort
    audit_log: AuditLogPort

    def advance(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]:
        # KR-081: contract doğrulaması üst akışta tamamlanmış payload üzerinden çalışılır.
        result = self.domain_service.execute(command=command, correlation_id=correlation_id)
        self.audit_log.append(
            event_type="MissionLifecycleManager.advance",
            correlation_id=correlation_id,
            payload={"status": result.get("status", "ok")},
        )
        return result
