# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-018: Calibration/QC hard gate coverage.
# KR-081: Contract-first assertions.

from __future__ import annotations

import uuid

import pytest

from src.core.domain.entities.analysis_job import AnalysisJobStatus


def test_ssot_v1_document_exists(ssot_v1_path: object) -> None:
    assert ssot_v1_path is not None, "SSOT v1.0.0 must exist as single canonical source."


def test_kr018_analysis_job_requires_calibration_before_start(analysis_job_entity: object) -> None:
    with pytest.raises(ValueError, match="KR-018|calibration"):
        analysis_job_entity.start_processing()


def test_kr018_analysis_job_starts_with_calibration(analysis_job_entity: object) -> None:
    analysis_job_entity.attach_calibration(uuid.uuid4())

    analysis_job_entity.start_processing()

    assert analysis_job_entity.status == AnalysisJobStatus.PROCESSING, (
        "Analysis job should transition to PROCESSING only when calibration evidence exists."
    )


def test_kr081_analysis_job_contract_fields_present(analysis_job_entity: object) -> None:
    payload = analysis_job_entity.__dict__

    assert "requires_calibrated" in payload, "KR-081 contract field missing: requires_calibrated"
    assert "calibration_record_id" in payload, "KR-081 contract field missing: calibration_record_id"
    assert payload["requires_calibrated"] is True


def test_api_endpoint_for_calibration_qc_unavailable_yet(fastapi_app_factory: object) -> None:
    if fastapi_app_factory is None:
        pytest.skip("FastAPI app factory bulunamadı; API endpoint integration testi skip edildi.")

    pytest.xfail("Calibration/QC endpointleri henüz implement değil; domain hard-gate doğrulandı.")
