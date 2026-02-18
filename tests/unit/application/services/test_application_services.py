# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003

import pytest

from src.application.services.calibration_gate_service import (
    CalibrationEvidence,
    CalibrationGateError,
    CalibrationGateService,
)
from src.application.services.contract_validator_service import ContractValidatorService
from src.application.services.planning_capacity import estimate_capacity
from src.application.services.qc_gate_service import QCDecision, QCEvidence, QCGateService


class _EvidenceStore:
    def __init__(self, evidence: CalibrationEvidence | None) -> None:
        self._evidence = evidence

    def get_latest_for_dataset(self, dataset_id: str) -> CalibrationEvidence | None:
        _ = dataset_id
        return self._evidence


class _SchemaRegistry:
    def __init__(self) -> None:
        self.schema: dict[str, object] = {
            "type": "object",
            "properties": {"job_id": {"type": "string"}},
            "required": ["job_id"],
            "additionalProperties": False,
        }

    def get_schema(self, schema_id: str) -> dict[str, object]:
        assert schema_id == "analysis_job"
        return self.schema


class _FakeJsonSchemaModule:
    class ValidationError(Exception):
        def __init__(self, message: str) -> None:
            super().__init__(message)
            self.path = []
            self.schema_path = []

    @staticmethod
    def validate(*, instance: object, schema: object) -> None:
        return None


def test_calibration_gate_blocks_without_evidence() -> None:
    gate = CalibrationGateService(store=_EvidenceStore(None))
    with pytest.raises(CalibrationGateError, match="KR-018"):
        gate.require_calibrated_and_qc_ok(dataset_id="d-1", correlation_id="c-1")


def test_contract_validator_valid_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(__import__("sys").modules, "jsonschema", _FakeJsonSchemaModule())
    validator = ContractValidatorService(registry=_SchemaRegistry())
    result = validator.validate(schema_id="analysis_job", payload={"job_id": "j-1"}, correlation_id="c-1")
    assert result.ok is True


def test_capacity_estimate_clamps_daily_capacity() -> None:
    estimate = estimate_capacity(1000.0, daily_capacity_donum=5000)
    assert estimate.daily_capacity_donum == 3000


def test_qc_decide_fail_on_missing_bands() -> None:
    service = QCGateService()
    decision = service.decide(
        QCEvidence(dataset_id="d-1", blur_ratio=0.05, missing_band_ratio=0.2, overlap_ok=True),
        correlation_id="c-1",
    )
    assert decision is QCDecision.FAIL
