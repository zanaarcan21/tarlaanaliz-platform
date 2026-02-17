# mypy: ignore-errors
from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.domain.entities.payment_intent import (
    PaymentIntent,
    PaymentMethod,
    PaymentProviderInfo,
    PaymentStatus,
    PaymentTargetType,
)
from src.infrastructure.persistence.models.payment_intent_model import PaymentIntentModel


class PaymentIntentRepository:
    """
    Minimal repo abstraction.
    Projede halihazırda repository/base pattern varsa, burayı ona adapte et.
    """

    def new_uuid(self) -> str:
        return str(uuid.uuid4())

    def insert(self, intent: PaymentIntent) -> None:
        raise NotImplementedError

    def update(self, intent: PaymentIntent) -> None:
        raise NotImplementedError

    def get_by_id(self, payment_intent_id: str) -> PaymentIntent:
        raise NotImplementedError

    def list_by_status(self, status: PaymentStatus, limit: int = 100) -> List[PaymentIntent]:
        raise NotImplementedError

    def list_expired_pending_ibans(self, now: datetime, limit: int = 500) -> List[PaymentIntent]:
        """Cron helper: PAYMENT_PENDING + IBAN_TRANSFER and expires_at < now."""
        raise NotImplementedError


class SqlAlchemyPaymentIntentRepository(PaymentIntentRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def insert(self, intent: PaymentIntent) -> None:
        m = self._to_model(intent)
        self.db.add(m)
        self.db.commit()

    def update(self, intent: PaymentIntent) -> None:
        m: PaymentIntentModel = self.db.get(PaymentIntentModel, uuid.UUID(intent.payment_intent_id))
        if not m:
            raise KeyError("payment_intent not found")
        self._apply_to_model(m, intent)
        self.db.commit()

    def get_by_id(self, payment_intent_id: str) -> PaymentIntent:
        m: PaymentIntentModel = self.db.get(PaymentIntentModel, uuid.UUID(payment_intent_id))
        if not m:
            raise KeyError("payment_intent not found")
        return self._to_entity(m)

    def list_by_status(self, status: PaymentStatus, limit: int = 100) -> List[PaymentIntent]:
        stmt = select(PaymentIntentModel).where(PaymentIntentModel.status == status.value).order_by(PaymentIntentModel.created_at.desc()).limit(limit)
        rows = self.db.execute(stmt).scalars().all()
        return [self._to_entity(r) for r in rows]

    def list_expired_pending_ibans(self, now: datetime, limit: int = 500) -> List[PaymentIntent]:
        stmt = (
            select(PaymentIntentModel)
            .where(PaymentIntentModel.status == PaymentStatus.PAYMENT_PENDING.value)
            .where(PaymentIntentModel.method == PaymentMethod.IBAN_TRANSFER.value)
            .where(PaymentIntentModel.expires_at.isnot(None))
            .where(PaymentIntentModel.expires_at < now)
            .order_by(PaymentIntentModel.expires_at.asc())
            .limit(limit)
        )
        rows = self.db.execute(stmt).scalars().all()
        return [self._to_entity(r) for r in rows]


    # --- mapping helpers ---

    def _to_model(self, intent: PaymentIntent) -> PaymentIntentModel:
        m = PaymentIntentModel()
        self._apply_to_model(m, intent)
        return m

    def _apply_to_model(self, m: PaymentIntentModel, intent: PaymentIntent) -> None:
        m.payment_intent_id = uuid.UUID(intent.payment_intent_id)
        m.payer_user_id = uuid.UUID(intent.payer_user_id)
        m.coop_id = uuid.UUID(intent.coop_id) if intent.coop_id else None

        m.target_type = intent.target_type.value
        m.target_id = uuid.UUID(intent.target_id)

        m.amount_kurus = intent.amount_kurus
        m.currency = intent.currency

        m.method = intent.method.value
        m.status = intent.status.value

        m.payment_ref = intent.payment_ref
        m.price_snapshot_id = uuid.UUID(intent.price_snapshot_id)

        if intent.provider:
            m.provider = intent.provider.name
            m.provider_session_id = intent.provider.session_id
            m.provider_payment_id = intent.provider.payment_id

        m.receipt_blob_id = intent.receipt_blob_id
        m.receipt_meta = intent.receipt_meta
        m.admin_notes = intent.admin_notes

        m.approved_by_admin_user_id = uuid.UUID(intent.approved_by_admin_user_id) if intent.approved_by_admin_user_id else None
        m.approved_at = intent.approved_at
        m.rejected_at = intent.rejected_at
        m.rejected_reason = intent.rejected_reason

        m.paid_at = intent.paid_at
        m.cancelled_at = intent.cancelled_at
        m.cancelled_reason = intent.cancelled_reason
        m.refunded_at = intent.refunded_at
        m.refund_amount_kurus = intent.refund_amount_kurus
        m.refund_reason = intent.refund_reason

        m.expires_at = intent.expires_at
        m.created_at = intent.created_at
        m.updated_at = intent.updated_at

    def _to_entity(self, m: PaymentIntentModel) -> PaymentIntent:
        provider = None
        if m.provider:
            provider = PaymentProviderInfo(name=m.provider, session_id=m.provider_session_id, payment_id=m.provider_payment_id)

        return PaymentIntent(
            payment_intent_id=str(m.payment_intent_id),
            payer_user_id=str(m.payer_user_id),
            coop_id=(str(m.coop_id) if m.coop_id else None),
            target_type=PaymentTargetType(m.target_type),
            target_id=str(m.target_id),
            amount_kurus=int(m.amount_kurus),
            currency=m.currency,
            method=PaymentMethod(m.method),
            status=PaymentStatus(m.status),
            payment_ref=m.payment_ref,
            price_snapshot_id=str(m.price_snapshot_id),
            provider=provider,
            receipt_blob_id=m.receipt_blob_id,
            receipt_meta=m.receipt_meta,
            admin_notes=m.admin_notes,
            approved_by_admin_user_id=(str(m.approved_by_admin_user_id) if m.approved_by_admin_user_id else None),
            approved_at=m.approved_at,
            rejected_at=m.rejected_at,
            rejected_reason=m.rejected_reason,
            paid_at=m.paid_at,
            cancelled_at=m.cancelled_at,
            cancelled_reason=m.cancelled_reason,
            refunded_at=m.refunded_at,
            refund_amount_kurus=(int(m.refund_amount_kurus) if m.refund_amount_kurus is not None else None),
            refund_reason=m.refund_reason,
            expires_at=m.expires_at,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
