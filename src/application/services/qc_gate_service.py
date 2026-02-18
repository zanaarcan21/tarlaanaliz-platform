# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-018: QC decisioning controls analysis start eligibility.

from __future__ import annotations

import enum
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class QCDecision(str, enum.Enum):
    PASS = "pass"  # noqa: S105
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

    def decide(self, ev: QCEvidence, *, correlation_id: str) -> QCDecision:
        if not ev.overlap_ok:
            logger.warning("qc_fail overlap dataset_id=%s correlation_id=%s", ev.dataset_id, correlation_id)
            return QCDecision.FAIL
        if ev.missing_band_ratio > self._missing_band_fail:
            logger.warning(
                "qc_fail missing_band dataset_id=%s ratio=%.3f correlation_id=%s",
                ev.dataset_id,
                ev.missing_band_ratio,
                correlation_id,
            )
            return QCDecision.FAIL
        if ev.blur_ratio > self._blur_fail:
            logger.warning(
                "qc_fail blur dataset_id=%s ratio=%.3f correlation_id=%s",
                ev.dataset_id,
                ev.blur_ratio,
                correlation_id,
            )
            return QCDecision.FAIL
        if ev.blur_ratio > self._blur_warn:
            logger.info(
                "qc_warn blur dataset_id=%s ratio=%.3f correlation_id=%s",
                ev.dataset_id,
                ev.blur_ratio,
                correlation_id,
            )
            return QCDecision.WARN
        logger.info("qc_pass dataset_id=%s correlation_id=%s", ev.dataset_id, correlation_id)
        return QCDecision.PASS
