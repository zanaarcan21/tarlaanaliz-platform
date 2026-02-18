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
