# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-033: Payment intents can target mission or subscription flows.

from __future__ import annotations

from src.application.dto.payment_intent_dto import PaymentIntentDTO


def test_from_dict_allows_missing_subscription_id() -> None:
    dto = PaymentIntentDTO.from_dict(
        {
            "intent_id": "intent-1",
            "payer_user_id": "user-1",
            "status": "pending",
            "amount": "12.50",
            "currency": "TRY",
            "requested_at": "2026-01-01T00:00:00Z",
        }
    )

    assert dto.subscription_id is None


def test_to_dict_preserves_null_subscription_id() -> None:
    dto = PaymentIntentDTO.from_dict(
        {
            "intent_id": "intent-2",
            "subscription_id": None,
            "payer_user_id": "user-1",
            "status": "pending",
            "amount": "9.99",
            "currency": "TRY",
            "requested_at": "2026-01-01T00:00:00Z",
        }
    )

    payload = dto.to_dict()

    assert payload["subscription_id"] is None
