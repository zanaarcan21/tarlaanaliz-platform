# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-018: Calibration and QC evidence is a hard gate before analysis start.
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
from typing import Protocol


@dataclass(frozen=True, slots=True)
class CalibrationEvidence:
    dataset_id: str
    is_calibrated: bool
    qc_status: str
    proof_uri: str | None = None


class CalibrationEvidenceStore(Protocol):
    def get_latest_for_dataset(self, dataset_id: str) -> CalibrationEvidence | None: ...


class CalibrationGateError(RuntimeError):
    pass


class CalibrationGateService:
    def __init__(self, store: CalibrationEvidenceStore) -> None:
        self._store = store

    def require_calibrated_and_qc_ok(self, *, dataset_id: str, correlation_id: str) -> CalibrationEvidence:
        _ = correlation_id
        evidence = self._store.get_latest_for_dataset(dataset_id)
        if evidence is None:
            raise CalibrationGateError("KR-018: calibration/QC evidence not found")
        if not evidence.is_calibrated:
            raise CalibrationGateError("KR-018: dataset is not calibrated")
        if evidence.qc_status not in {"pass", "warn"}:
            raise CalibrationGateError(f"KR-018: QC status not acceptable ({evidence.qc_status})")
        return evidence
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
