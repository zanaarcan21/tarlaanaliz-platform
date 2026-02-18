# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-018, KR-033, KR-081: Farmer end-to-end domain journey.

from __future__ import annotations

import os
import uuid

import pytest

from src.core.domain.entities.analysis_job import AnalysisJobStatus

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        os.getenv("RUN_E2E") != "1" and os.getenv("E2E") != "1",
        reason="E2E tests disabled. Set RUN_E2E=1 or E2E=1.",
    ),
]


def test_farmer_journey_payment_then_analysis(
    field_entity: object,
    mission_entity: object,
    subscription_entity: object,
    payment_intent_entity: object,
    analysis_job_entity: object,
) -> None:
    # Arrange/Act: payment intent + manual approval (KR-033)
    payment_intent_entity.receipt_blob_id = "blob://dekont-001"
    payment_intent_entity.mark_paid(approved_by_admin_user_id=uuid.uuid4())

    # Act: mission assignment and upload pipeline
    mission_entity.assign_pilot(uuid.uuid4())
    mission_entity.acknowledge()
    mission_entity.mark_flown()
    mission_entity.mark_uploaded()

    # KR-018 calibration hard gate
    analysis_job_entity.attach_calibration(uuid.uuid4())
    analysis_job_entity.start_processing()

    # Assert
    assert payment_intent_entity.status.value == "PAID"
    assert mission_entity.status.value == "UPLOADED"
    assert analysis_job_entity.status == AnalysisJobStatus.PROCESSING
    assert subscription_entity.status.value in {"PENDING_PAYMENT", "ACTIVE"}
    assert field_entity.geometry["type"] == "Polygon", "KR-081 contract field check failed."
