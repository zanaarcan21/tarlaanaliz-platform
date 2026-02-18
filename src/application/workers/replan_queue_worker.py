# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Queue worker retries replan tasks with ack/nack semantics.

from __future__ import annotations

import time
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


@dataclass(frozen=True, slots=True)
class ReplanTask:
    task_id: str
    mission_id: str
    reason: str
    correlation_id: str


class QueueClient(Protocol):
    def pop(self, queue_name: str) -> ReplanTask | None: ...

    def ack(self, queue_name: str, task_id: str) -> None: ...

    def nack(self, queue_name: str, task_id: str, *, requeue: bool) -> None: ...


class MissionReplanner(Protocol):
    def replan(self, *, mission_id: str, reason: str, correlation_id: str) -> None: ...


class ReplanQueueWorker:
    def __init__(self, *, queue: QueueClient, replanner: MissionReplanner, queue_name: str = "replan") -> None:
        self._queue = queue
        self._replanner = replanner
        self._queue_name = queue_name

    def run_once(self) -> bool:
        task = self._queue.pop(self._queue_name)
        if task is None:
            return False
        try:
            self._replanner.replan(mission_id=task.mission_id, reason=task.reason, correlation_id=task.correlation_id)
            self._queue.ack(self._queue_name, task.task_id)
            return True
        except Exception:
            self._queue.nack(self._queue_name, task.task_id, requeue=True)
            return True

    def run_forever(self, *, poll_interval_s: float = 1.0) -> None:
        while True:
            if not self.run_once():
                time.sleep(float(poll_interval_s))
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
