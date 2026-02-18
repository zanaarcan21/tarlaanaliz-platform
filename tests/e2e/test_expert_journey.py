# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-081: Expert workflow contract checks.

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

import pytest

from src.core.domain.entities.audit_log_entry import AuditLogEntry

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        os.getenv("RUN_E2E") != "1" and os.getenv("E2E") != "1",
        reason="E2E tests disabled. Set RUN_E2E=1 or E2E=1.",
    ),
]


def test_expert_journey_review_and_audit(expert_entity: object, analysis_job_entity: object) -> None:
    analysis_job_entity.attach_calibration(uuid.uuid4())
    analysis_job_entity.start_processing()
    analysis_job_entity.complete()

    review_audit = AuditLogEntry(
        audit_log_id=uuid.uuid4(),
        event_type="RESULT",
        event_action="FINISH",
        outcome="SUCCESS",
        correlation_id="corr_expert_review_1",
        actor_type="system",
        actor_id_hash="hash_expert_001",
        created_at=datetime(2026, 1, 1, 13, 0, tzinfo=timezone.utc),
        resource_type="analysis_job",
        resource_id=analysis_job_entity.analysis_job_id,
        change_details={"expert_id": str(expert_entity.expert_id), "decision": "approve"},
    )

    assert analysis_job_entity.status.value == "COMPLETED"
    assert review_audit.change_details["decision"] == "approve"
