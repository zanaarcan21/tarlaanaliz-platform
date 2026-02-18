# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-018: Calibration and QC evidence is a hard gate before analysis start.

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
