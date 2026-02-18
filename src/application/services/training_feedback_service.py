# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-071: Feedback flow is one-way into platform persistence and outbound events.
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Training feedback orkestrasyon servisi.
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
class TrainingFeedback:
    feedback_id: str
    dataset_id: str
    label_issue: str
    note: str


class TrainingFeedbackRepository(Protocol):
    def append(self, feedback: TrainingFeedback) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class TrainingFeedbackService:
    def __init__(self, repo: TrainingFeedbackRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def submit(self, *, feedback: TrainingFeedback, correlation_id: str) -> None:
        self._repo.append(feedback)
        self._bus.publish(
            "training_feedback.submitted",
            {
                "feedback_id": feedback.feedback_id,
                "dataset_id": feedback.dataset_id,
                "label_issue": feedback.label_issue,
            },
            correlation_id=correlation_id,
        )
class DomainServicePort(Protocol):
    def execute(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]: ...


class AuditLogPort(Protocol):
    def append(self, *, event_type: str, correlation_id: str, payload: dict[str, Any]) -> None: ...


@dataclass(slots=True)
class TrainingFeedbackService:
    domain_service: DomainServicePort
    audit_log: AuditLogPort

    def orchestrate(self, *, command: dict[str, Any], correlation_id: str) -> dict[str, Any]:
        # KR-081: contract doğrulaması üst akışta tamamlanmış payload üzerinden çalışılır.
        result = self.domain_service.execute(command=command, correlation_id=correlation_id)
        self.audit_log.append(
            event_type="TrainingFeedbackService.orchestrate",
            correlation_id=correlation_id,
            payload={"status": result.get("status", "ok")},
        )
        return result
