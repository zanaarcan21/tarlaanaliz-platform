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
# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

from src.application.services.calibration_gate_service import CalibrationGateError, CalibrationGateService
from src.application.services.contract_validator_service import ContractValidatorService
from src.application.services.planning_capacity import PlanningCapacityService
from src.application.services.qc_gate_service import QcGateDecision, QcGateError, QcGateService, QcStatus


class _CalibrationEvidence:
    def __init__(self, verified: bool) -> None:
        self.verified = verified

    def is_calibration_verified(self, *, mission_id: str) -> bool:  # noqa: ARG002
        return self.verified


class _SchemaValidator:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def validate(self, *, schema_name: str, payload: dict[str, object]) -> None:
        self.calls.append((schema_name, payload))


def test_calibration_gate_blocks_when_not_verified() -> None:
    service = CalibrationGateService(evidence_port=_CalibrationEvidence(verified=False))
    try:
        service.assert_ready(mission_id="m-1")
        raise AssertionError("expected CalibrationGateError")
    except CalibrationGateError:
        assert True


def test_contract_validator_delegates_to_schema_port() -> None:
    validator = _SchemaValidator()
    service = ContractValidatorService(schema_port=validator)

    payload = {"job_id": "a-1"}
    service.validate_payload(schema_name="analysis_job", payload=payload)

    assert validator.calls == [("analysis_job", payload)]


def test_planning_capacity_computes_pilot_requirement() -> None:
    service = PlanningCapacityService(effort_per_donum=2.0, max_daily_effort_per_pilot=100.0)

    plan = service.calculate(area_donum=120.0)

    assert plan.effort_points == 240.0
    assert plan.required_pilots == 3


def test_qc_gate_blocks_fail_status() -> None:
    service = QcGateService()
    decision = QcGateDecision(status=QcStatus.FAIL, reason="missing_control_strip")

    try:
        service.assert_analysis_allowed(decision)
        raise AssertionError("expected QcGateError")
    except QcGateError as exc:
        assert str(exc) == "missing_control_strip"
