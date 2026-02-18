# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for user payloads (PII-minimized)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class UserDTO:
    """User DTO for app-layer identity references."""

    user_id: str
    phone: str
    role: str
    status: str
    full_name: str | None
    created_at: datetime
    updated_at: datetime

    # PIN, OTP, email and TCKN are intentionally excluded from DTO payload.
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "phone": self.phone,
            "role": self.role,
            "status": self.status,
            "full_name": self.full_name,
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "UserDTO":
        return cls(
            user_id=str(payload["user_id"]),
            phone=str(payload["phone"]),
            role=str(payload["role"]),
            status=str(payload["status"]),
            full_name=None if payload.get("full_name") is None else str(payload["full_name"]),
            created_at=_parse_datetime(payload["created_at"]),
            updated_at=_parse_datetime(payload["updated_at"]),
        )


def _to_utc_iso(value: datetime) -> str:
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
