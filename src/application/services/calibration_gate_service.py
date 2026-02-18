# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-018: Calibration + QC evidence is a hard gate for analysis start.

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

logger = logging.getLogger(__name__)


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
        ev = self._store.get_latest_for_dataset(dataset_id)
        if ev is None:
            logger.warning("calibration_gate_missing dataset_id=%s correlation_id=%s", dataset_id, correlation_id)
            raise CalibrationGateError("KR-018: calibration/QC evidence not found")
        if not ev.is_calibrated:
            logger.warning(
                "calibration_gate_not_calibrated dataset_id=%s correlation_id=%s",
                dataset_id,
                correlation_id,
            )
            raise CalibrationGateError("KR-018: dataset is not calibrated")
        if ev.qc_status not in {"pass", "warn"}:
            logger.warning(
                "calibration_gate_qc_fail dataset_id=%s qc=%s correlation_id=%s",
                dataset_id,
                ev.qc_status,
                correlation_id,
            )
            raise CalibrationGateError(f"KR-018: QC status not acceptable ({ev.qc_status})")
        logger.info(
            "calibration_gate_ok dataset_id=%s qc=%s correlation_id=%s",
            dataset_id,
            ev.qc_status,
            correlation_id,
        )
        return ev
