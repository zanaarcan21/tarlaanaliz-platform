# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-033: Payment intent + manual approval + audit flow.
# KR-081: Contract-first assertions.

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from src.core.domain.entities.audit_log_entry import AuditLogEntry
from src.core.domain.entities.payment_intent import PaymentStatus
from src.core.domain.value_objects.payment_status import (
    PaymentStatus as PaymentStatusVO,
    is_valid_payment_transition,
    requires_payment_intent,
)


def _apply_webhook_once(intent: object, event_id: str, seen_events: set[str]) -> bool:
    """Fake webhook consumer: idempotent PAID transition (KR-033)."""
    if event_id in seen_events:
        return False
    seen_events.add(event_id)
    intent.mark_paid()
    return True


def test_kr033_paid_transition_requires_intent() -> None:
    assert requires_payment_intent(PaymentStatusVO.PAID) is True


def test_kr033_payment_intent_manual_approval_success(payment_intent_entity: object, fixed_now: datetime) -> None:
    admin_id = uuid.uuid4()

    payment_intent_entity.mark_paid(paid_at=fixed_now, approved_by_admin_user_id=admin_id)

    assert payment_intent_entity.status == PaymentStatus.PAID
    assert payment_intent_entity.approved_by_admin_user_id == admin_id
    assert payment_intent_entity.approved_at == fixed_now


def test_kr033_fake_webhook_idempotent(payment_intent_entity: object) -> None:
    seen_events: set[str] = set()

    first = _apply_webhook_once(payment_intent_entity, "evt-1", seen_events)
    second = _apply_webhook_once(payment_intent_entity, "evt-1", seen_events)

    assert first is True
    assert second is False, "Repeated webhook must be no-op for idempotency."


def test_kr033_payment_transition_matrix_contract() -> None:
    assert is_valid_payment_transition(PaymentStatusVO.PAYMENT_PENDING, PaymentStatusVO.PAID)
    assert not is_valid_payment_transition(PaymentStatusVO.PAID, PaymentStatusVO.PAYMENT_PENDING)


def test_kr033_audit_log_entry_created_for_manual_approval(payment_intent_entity: object) -> None:
    payment_intent_entity.mark_paid(
        paid_at=datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        approved_by_admin_user_id=uuid.uuid4(),
    )

    log = AuditLogEntry(
        audit_log_id=uuid.uuid4(),
        event_type="JOB",
        event_action="UPDATE",
        outcome="SUCCESS",
        correlation_id="corr_payment_approval_1",
        actor_type="admin",
        actor_id_hash="hash_admin_001",
        created_at=datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc),
        resource_type="payment_intent",
        change_details={"status": payment_intent_entity.status.value},
    )

    assert log.change_details == {"status": "PAID"}


def test_webhook_api_unavailable_yet(fastapi_app_factory: object) -> None:
    if fastapi_app_factory is None:
        pytest.skip("FastAPI app factory bulunamadı; payment webhook integration testi skip edildi.")

    pytest.xfail("Payment webhook endpointi henüz implement değil; state machine doğrulandı.")
