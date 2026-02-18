# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for payment intent flows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, slots=True)
class PaymentProofRefDTO:
    """Reference-only payment proof metadata (PII minimized)."""

    proof_id: str
    proof_type: str
    uri: str

    def to_dict(self) -> dict[str, Any]:
        return {"proof_id": self.proof_id, "proof_type": self.proof_type, "uri": self.uri}

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PaymentProofRefDTO":
        return cls(
            proof_id=str(payload["proof_id"]),
            proof_type=str(payload["proof_type"]),
            uri=str(payload["uri"]),
        )


@dataclass(frozen=True, slots=True)
class PaymentIntentDTO:
    """Payment intent DTO aligned with manual approval flow."""

    intent_id: str
    subscription_id: str
    payer_user_id: str
    status: str
    amount: Decimal
    currency: str
    requested_at: datetime
    receipt_refs: tuple[PaymentProofRefDTO, ...]
    approved_by_user_id: str | None
    approved_at: datetime | None
    rejected_by_user_id: str | None
    rejected_at: datetime | None
    reject_reason: str | None
    audit_log_ref: str | None

    # KR-033: paid transition requires a valid payment intent and manual approval evidence.
    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "subscription_id": self.subscription_id,
            "payer_user_id": self.payer_user_id,
            "status": self.status,
            "amount": str(self.amount),
            "currency": self.currency,
            "requested_at": _to_utc_iso(self.requested_at),
            "receipt_refs": [item.to_dict() for item in self.receipt_refs],
            "approved_by_user_id": self.approved_by_user_id,
            "approved_at": _optional_dt(self.approved_at),
            "rejected_by_user_id": self.rejected_by_user_id,
            "rejected_at": _optional_dt(self.rejected_at),
            "reject_reason": self.reject_reason,
            "audit_log_ref": self.audit_log_ref,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PaymentIntentDTO":
        return cls(
            intent_id=str(payload["intent_id"]),
            subscription_id=str(payload["subscription_id"]),
            payer_user_id=str(payload["payer_user_id"]),
            status=str(payload["status"]),
            amount=Decimal(str(payload["amount"])),
            currency=str(payload["currency"]),
            requested_at=_parse_datetime(payload["requested_at"]),
            receipt_refs=tuple(
                PaymentProofRefDTO.from_dict(item) for item in payload.get("receipt_refs", [])
            ),
            approved_by_user_id=_to_optional_str(payload.get("approved_by_user_id")),
            approved_at=_parse_optional_datetime(payload.get("approved_at")),
            rejected_by_user_id=_to_optional_str(payload.get("rejected_by_user_id")),
            rejected_at=_parse_optional_datetime(payload.get("rejected_at")),
            reject_reason=_to_optional_str(payload.get("reject_reason")),
            audit_log_ref=_to_optional_str(payload.get("audit_log_ref")),
        )


def _to_optional_str(value: Any) -> str | None:
    return None if value is None else str(value)


def _to_utc_iso(value: datetime) -> str:
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _optional_dt(value: datetime | None) -> str | None:
    return None if value is None else _to_utc_iso(value)


def _parse_optional_datetime(raw: Any) -> datetime | None:
    return None if raw is None else _parse_datetime(raw)


def _parse_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    text = str(raw)
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
