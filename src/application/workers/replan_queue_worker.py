# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Replan kuyruğundaki Mission'lar için alternatif slot/pilot arama.
Sorumluluk: Queue worker; arka plan işleri tüketir ve idempotent şekilde işler.
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


class ReplanQueuePort(Protocol):
    def dequeue(self) -> dict[str, str] | None: ...


class ReplanServicePort(Protocol):
    def replan(self, *, mission_id: str, correlation_id: str) -> None: ...


@dataclass(slots=True)
class ReplanQueueWorker:
    queue_port: ReplanQueuePort
    replan_service: ReplanServicePort

    def run_once(self) -> bool:
        message = self.queue_port.dequeue()
        if message is None:
            return False

        mission_id = message.get("mission_id")
        correlation_id = message.get("correlation_id", "")
        if not mission_id:
            return False

        # KR-015: replan akışı kapasite/pencere kurallarıyla uyumlu uygulama servisine devredilir.
        self.replan_service.replan(mission_id=mission_id, correlation_id=correlation_id)
        return True
