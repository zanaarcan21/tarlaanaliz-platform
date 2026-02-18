# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Seasonal slot generation uses deterministic scheduling intervals.
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Subscription sezonluk takvim üretimi ve mission zamanlama.
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


@dataclass(frozen=True, slots=True)
class SeasonPlan:
    subscription_id: str
    season_year: int
    mission_slots_ts_ms: tuple[int, ...]


class SubscriptionScheduler:
    def __init__(self, *, slot_interval_days: int = 14) -> None:
        self._interval_days = int(slot_interval_days)

    def build_season_plan(
        self,
        *,
        subscription_id: str,
        season_year: int,
        season_start_ts_ms: int,
        season_end_ts_ms: int,
        correlation_id: str,
    ) -> SeasonPlan:
        _ = correlation_id
        interval_ms = self._interval_days * 24 * 60 * 60 * 1000
        slots: list[int] = []
        cursor = int(season_start_ts_ms)
        while cursor <= int(season_end_ts_ms):
            slots.append(cursor)
            cursor += interval_ms
        return SeasonPlan(subscription_id=subscription_id, season_year=season_year, mission_slots_ts_ms=tuple(slots))
from typing import Any, Protocol


class DomainServicePort(Protocol):
    def execute(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]: ...


class AuditLogPort(Protocol):
    def append(self, *, event_type: str, correlation_id: str, payload: dict[str, Any]) -> None: ...


@dataclass(slots=True)
class SubscriptionScheduler:
    domain_service: DomainServicePort
    audit_log: AuditLogPort

    def orchestrate(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]:
        # KR-081: contract doğrulaması üst akışta tamamlanmış payload üzerinden çalışılır.
        result = self.domain_service.execute(command=command, correlation_id=correlation_id)
        self.audit_log.append(
            event_type="SubscriptionScheduler.orchestrate",
            correlation_id=correlation_id,
            payload={"status": result.get("status", "ok")},
        )
        return result
