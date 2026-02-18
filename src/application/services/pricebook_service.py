# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Pricebook snapshots use typed contracts at application boundaries.
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: PriceBook/PriceSnapshot yönetimi (KR-022).
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
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PriceSnapshot:
    snapshot_id: str
    currency: str
    valid_from_ts_ms: int
    items: dict[str, int]


class PricebookRepository(Protocol):
    def upsert_snapshot(self, snap: PriceSnapshot) -> None: ...

    def get_active_snapshot(self, *, at_ts_ms: int) -> PriceSnapshot | None: ...

    def list_snapshots(self, *, limit: int) -> tuple[PriceSnapshot, ...]: ...


class PricebookService:
    def __init__(self, repo: PricebookRepository) -> None:
        self._repo = repo

    def publish_snapshot(self, *, snap: PriceSnapshot, correlation_id: str) -> None:
        _ = correlation_id
        self._repo.upsert_snapshot(snap)

    def get_active(self, *, at_ts_ms: int) -> PriceSnapshot | None:
        return self._repo.get_active_snapshot(at_ts_ms=at_ts_ms)

    def list_recent(self, *, limit: int = 50) -> tuple[PriceSnapshot, ...]:
        return self._repo.list_snapshots(limit=limit)
from typing import Any, Protocol


class DomainServicePort(Protocol):
    def execute(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]: ...


class AuditLogPort(Protocol):
    def append(self, *, event_type: str, correlation_id: str, payload: dict[str, Any]) -> None: ...


@dataclass(slots=True)
class PricebookService:
    domain_service: DomainServicePort
    audit_log: AuditLogPort

    def orchestrate(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]:
        # KR-081: contract doğrulaması üst akışta tamamlanmış payload üzerinden çalışılır.
        result = self.domain_service.execute(command=command, correlation_id=correlation_id)
        self.audit_log.append(
            event_type="PricebookService.orchestrate",
            correlation_id=correlation_id,
            payload={"status": result.get("status", "ok")},
        )
        return result
