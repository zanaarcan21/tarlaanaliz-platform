# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for contract-first payload mapping."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class SubscriptionDTO:
    subscription_id: str
    user_ref: str
    plan_code: str
    status: str
    current_period_start_at: datetime
    current_period_end_at: datetime
    payment_intent_id: str | None
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        # KR-033: paid state requires payment intent presence.
        if self.status == "paid" and self.payment_intent_id is None:
            raise ValueError("payment_intent_id is required when status is 'paid'")

    # KR-033: status='paid' contract consumers must also observe non-null payment_intent_id.
    def to_dict(self) -> dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "user_ref": self.user_ref,
            "plan_code": self.plan_code,
            "status": self.status,
            "current_period_start_at": _to_utc_iso(self.current_period_start_at),
            "current_period_end_at": _to_utc_iso(self.current_period_end_at),
            "payment_intent_id": self.payment_intent_id,
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> SubscriptionDTO:
        return cls(
            subscription_id=str(payload["subscription_id"]),
            user_ref=str(payload["user_ref"]),
            plan_code=str(payload["plan_code"]),
            status=str(payload["status"]),
            current_period_start_at=_parse_datetime(payload["current_period_start_at"]),
            current_period_end_at=_parse_datetime(payload["current_period_end_at"]),
            payment_intent_id=None if payload.get("payment_intent_id") is None else str(payload["payment_intent_id"]),
            created_at=_parse_datetime(payload["created_at"]),
            updated_at=_parse_datetime(payload["updated_at"]),
        )


def _to_utc_iso(value: datetime) -> str:
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
