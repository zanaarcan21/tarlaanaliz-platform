# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: KR-018 'Tam Radyometrik Kalibrasyon' hard gate'i.
Sorumluluk: Use-case orkestrasyonu; domain service + ports birleşimi; policy enforcement.
Girdi/Çıktı (Contract/DTO/Event): Girdi: API/Job/Worker tetiklemesi. Çıktı: DTO, event, state transition.
Güvenlik (RBAC/PII/Audit): RBAC burada; PII redaction; audit log; rate limit (gereken yerde).
Hata Modları (idempotency/retry/rate limit): 400/403/409/429/5xx mapping; retry-safe tasarım; idempotency key/hard gate’ler.
Observability (log fields/metrics/traces): correlation_id, latency, error_code; use-case metric sayaçları.
Testler: Unit + integration; kritik akış için e2e (özellikle ödeme/planlama/kalibrasyon).
Bağımlılıklar: Domain + ports + infra implementasyonları + event bus.
Notlar/SSOT: Contract-first (KR-081) ve kritik kapılar (KR-018/KR-033/KR-015) application katmanında enforce edilir. KR-018 hard gate: calibrated/QC kanıtı olmadan AnalysisJob başlatılmamalıdır.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol



class CalibrationEvidencePort(Protocol):
    def is_calibration_verified(self, *, mission_id: str) -> bool: ...


class CalibrationGateError(PermissionError):
    pass


@dataclass(slots=True)
class CalibrationGateService:
    evidence_port: CalibrationEvidencePort

    def assert_ready(self, *, mission_id: str) -> None:
        # KR-018: kalibrasyon kanıtı yoksa akış hard-fail olmalıdır.
        if not self.evidence_port.is_calibration_verified(mission_id=mission_id):
            raise CalibrationGateError("calibration_hard_gate_failed")
