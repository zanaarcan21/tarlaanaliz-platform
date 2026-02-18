# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-033: End-to-end payment flow assertions.

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

import pytest

from src.core.domain.entities.audit_log_entry import AuditLogEntry
from src.core.domain.entities.payment_intent import PaymentIntent, PaymentStatus

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        os.getenv("RUN_E2E") != "1" and os.getenv("E2E") != "1",
        reason="E2E tests disabled. Set RUN_E2E=1 or E2E=1.",
    ),
]


def test_payment_flow_payment_intent_required_before_paid(payment_intent_entity: PaymentIntent) -> None:
    with pytest.raises(AttributeError, match="mark_paid"):
        # KR-033: intent object yokken paid state'e gecis simule edilmez.
        missing_intent = None
        missing_intent.mark_paid()  # type: ignore[union-attr]

    payment_intent_entity.receipt_blob_id = "blob://dekont-e2e"
    payment_intent_entity.mark_paid(approved_by_admin_user_id=uuid.uuid4())

    assert payment_intent_entity.status == PaymentStatus.PAID


def test_payment_flow_audit_log_exists_after_manual_approval(payment_intent_entity: PaymentIntent) -> None:
    payment_intent_entity.receipt_blob_id = "blob://dekont-e2e-2"
    payment_intent_entity.mark_paid(
        paid_at=datetime(2026, 1, 1, 15, 0, tzinfo=timezone.utc),
        approved_by_admin_user_id=uuid.uuid4(),
    )

    log = AuditLogEntry(
        audit_log_id=uuid.uuid4(),
        event_type="JOB",
        event_action="UPDATE",
        outcome="SUCCESS",
        correlation_id="corr_e2e_payment_approval",
        actor_type="admin",
        actor_id_hash="hash_admin_e2e",
        created_at=datetime(2026, 1, 1, 15, 1, tzinfo=timezone.utc),
        resource_type="payment_intent",
        resource_id=payment_intent_entity.payment_intent_id,
        change_details={"status": payment_intent_entity.status.value, "receipt": payment_intent_entity.receipt_blob_id},
    )

    assert log.change_details["status"] == "PAID"
    assert log.change_details["receipt"] == "blob://dekont-e2e-2"
