# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-018: QC decisioning blocks invalid datasets from analysis.

from __future__ import annotations

import enum
from dataclasses import dataclass


class QCDecision(str, enum.Enum):
    PASS = "pass"  # noqa: S105
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: QC gate değerlendirme (pass/warn/fail).
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
from enum import Enum


class QcStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass(frozen=True, slots=True)
class QCEvidence:
    dataset_id: str
    blur_ratio: float
    missing_band_ratio: float
    overlap_ok: bool
    notes: str | None = None


class QCGateService:
    def __init__(
        self,
        *,
        blur_fail_threshold: float = 0.35,
        blur_warn_threshold: float = 0.20,
        missing_band_fail_threshold: float = 0.05,
    ) -> None:
        self._blur_fail = blur_fail_threshold
        self._blur_warn = blur_warn_threshold
        self._missing_band_fail = missing_band_fail_threshold

    def decide(self, evidence: QCEvidence, *, correlation_id: str) -> QCDecision:
        _ = correlation_id
        if not evidence.overlap_ok:
            return QCDecision.FAIL
        if evidence.missing_band_ratio > self._missing_band_fail:
            return QCDecision.FAIL
        if evidence.blur_ratio > self._blur_fail:
            return QCDecision.FAIL
        if evidence.blur_ratio > self._blur_warn:
            return QCDecision.WARN
        return QCDecision.PASS
class QcGateError(PermissionError):
    pass


@dataclass(frozen=True, slots=True)
class QcGateDecision:
    status: QcStatus
    reason: str | None = None


@dataclass(slots=True)
class QcGateService:
    def assert_analysis_allowed(self, decision: QcGateDecision) -> None:
        # KR-018: QC sonucu fail olduğunda analysis başlatma hard-gate ile engellenir.
        if decision.status == QcStatus.FAIL:
            raise QcGateError(decision.reason or "qc_hard_gate_failed")
