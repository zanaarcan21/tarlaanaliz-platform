# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/payment_webhook_schemas.py
# DESC: Webhook payload doğrulama schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class WebhookEventType(str, Enum):
    payment_intent_created = "payment_intent.created"
    payment_intent_succeeded = "payment_intent.succeeded"
    payment_intent_failed = "payment_intent.failed"
    refund_created = "refund.created"


class PaymentIntentStatus(str, Enum):
    requires_payment_method = "requires_payment_method"
    requires_confirmation = "requires_confirmation"
    processing = "processing"
    succeeded = "succeeded"
    failed = "failed"


class CurrencyCode(str, Enum):
    try_ = "TRY"
    usd = "USD"
    eur = "EUR"


class PaymentIntentPayload(SchemaBase):
    payment_intent_id: str = Field(min_length=3, max_length=128)
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    currency: CurrencyCode
    status: PaymentIntentStatus
    reference: str = Field(min_length=2, max_length=128)
    bank_receipt_id: str | None = Field(default=None, min_length=2, max_length=128)


class RefundPayload(SchemaBase):
    refund_id: str = Field(min_length=3, max_length=128)
    payment_intent_id: str = Field(min_length=3, max_length=128)
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    currency: CurrencyCode
    reason: str | None = Field(default=None, max_length=256)


class WebhookEventRequest(SchemaBase):
    # KR-033: webhook processing requires auditable event_id and explicit payment payload contract.
    event_id: str = Field(min_length=3, max_length=128)
    event_type: WebhookEventType
    occurred_at: datetime
    idempotency_key: str | None = Field(default=None, min_length=3, max_length=128)
    payment_intent: PaymentIntentPayload | None = None
    refund: RefundPayload | None = None
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class WebhookAckResponse(SchemaBase):
    received: bool
    deduplicated: bool
    event_id: str = Field(min_length=3, max_length=128)
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
