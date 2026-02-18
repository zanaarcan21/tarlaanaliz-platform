# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003

import sys

import pytest

from src.application.services.calibration_gate_service import (
    CalibrationEvidence,
    CalibrationGateError,
    CalibrationGateService,
)
from src.application.services.contract_validator_service import ContractValidatorService
from src.application.services.planning_capacity import estimate_capacity, estimate_daily_capacity
from src.application.services.qc_gate_service import QCDecision, QCEvidence, QCGateService


class _EvidenceStore:
    def __init__(self, evidence: CalibrationEvidence | None) -> None:
        self._evidence = evidence

    def get_latest_for_dataset(self, dataset_id: str) -> CalibrationEvidence | None:
        _ = dataset_id
        return self._evidence


class _SchemaRegistry:
    def get_schema(self, schema_id: str) -> dict[str, object]:
        assert schema_id == "analysis_job"
        return {
            "type": "object",
            "properties": {"job_id": {"type": "string"}},
            "required": ["job_id"],
            "additionalProperties": False,
        }


class _FakeJsonschema:
    class ValidationError(Exception):
        def __init__(self, message: str) -> None:
            super().__init__(message)
            self.path = []
            self.schema_path = []

    @staticmethod
    def validate(*, instance: object, schema: object) -> None:
        if not isinstance(instance, dict) or "job_id" not in instance:
            raise _FakeJsonschema.ValidationError("job_id is required")


def test_calibration_gate_blocks_without_evidence() -> None:
    gate = CalibrationGateService(store=_EvidenceStore(None))
    with pytest.raises(CalibrationGateError, match="KR-018"):
        gate.require_calibrated_and_qc_ok(dataset_id="d-1", correlation_id="c-1")


def test_contract_validator_valid_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "jsonschema", _FakeJsonschema())
    validator = ContractValidatorService(registry=_SchemaRegistry())
    result = validator.validate(schema_id="analysis_job", payload={"job_id": "j-1"}, correlation_id="c-1")
    assert result.ok is True


def test_contract_validator_invalid_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "jsonschema", _FakeJsonschema())
    validator = ContractValidatorService(registry=_SchemaRegistry())
    result = validator.validate(schema_id="analysis_job", payload={}, correlation_id="c-1")
    assert result.ok is False
    assert result.error is not None


def test_capacity_estimation_clamps_requested_daily_capacity() -> None:
    assert estimate_daily_capacity(requested=5000) == 3000
    assert estimate_capacity(1000.0, daily_capacity_donum=5000).daily_capacity_donum == 3000


def test_qc_decision_fails_for_missing_bands() -> None:
    service = QCGateService()
    decision = service.decide(
        QCEvidence(dataset_id="d-1", blur_ratio=0.05, missing_band_ratio=0.20, overlap_ok=True),
        correlation_id="c-1",
    )
    assert decision is QCDecision.FAIL
