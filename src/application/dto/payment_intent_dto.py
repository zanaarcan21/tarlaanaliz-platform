# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for contract-first payload mapping."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class PaymentProofRefDTO:
    proof_id: str
    file_uri: str


@dataclass(frozen=True, slots=True)
class PaymentIntentDTO:
    payment_intent_id: str
    payer_ref: str
    currency_code: str
    amount_minor: int
    status: str
    proof_refs: tuple[PaymentProofRefDTO, ...]
    approved_by_user_id: str | None
    created_at: datetime
    approved_at: datetime | None

    def __post_init__(self) -> None:
        # KR-033: paid state requires explicit manual approval evidence.
        if self.status == "paid" and self.approved_at is None:
            raise ValueError("approved_at is required when status is 'paid'")

    # KR-033: paid state is valid only with payment_intent_id present in contract.
    def to_dict(self) -> dict[str, Any]:
        return {
            "payment_intent_id": self.payment_intent_id,
            "payer_ref": self.payer_ref,
            "currency_code": self.currency_code,
            "amount_minor": self.amount_minor,
            "status": self.status,
            "proof_refs": [{"proof_id": ref.proof_id, "file_uri": ref.file_uri} for ref in self.proof_refs],
            "approved_by_user_id": self.approved_by_user_id,
            "created_at": _to_utc_iso(self.created_at),
            "approved_at": _optional_dt(self.approved_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> PaymentIntentDTO:
        return cls(
            payment_intent_id=str(payload["payment_intent_id"]),
            payer_ref=str(payload["payer_ref"]),
            currency_code=str(payload["currency_code"]),
            amount_minor=int(payload["amount_minor"]),
            status=str(payload["status"]),
            proof_refs=tuple(
                PaymentProofRefDTO(proof_id=str(item["proof_id"]), file_uri=str(item["file_uri"]))
                for item in payload.get("proof_refs", [])
            ),
            approved_by_user_id=(
                None if payload.get("approved_by_user_id") is None else str(payload["approved_by_user_id"])
            ),
            created_at=_parse_datetime(payload["created_at"]),
            approved_at=_parse_optional_datetime(payload.get("approved_at")),
        )


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
    parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
