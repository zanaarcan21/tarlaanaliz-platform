# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for pilot payloads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class PilotDTO:
    """Pilot profile DTO used by planning and mission assignment."""

    pilot_id: str
    display_name: str
    phone: str
    territory_id: str
    daily_capacity: int
    reliability_score: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # KR-015: planning capacity inputs remain explicit.
    def to_dict(self) -> dict[str, Any]:
        return {
            "pilot_id": self.pilot_id,
            "display_name": self.display_name,
            "phone": self.phone,
            "territory_id": self.territory_id,
            "daily_capacity": self.daily_capacity,
            "reliability_score": self.reliability_score,
            "is_active": self.is_active,
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PilotDTO":
        return cls(
            pilot_id=str(payload["pilot_id"]),
            display_name=str(payload["display_name"]),
            phone=str(payload["phone"]),
            territory_id=str(payload["territory_id"]),
            daily_capacity=int(payload["daily_capacity"]),
            reliability_score=float(payload["reliability_score"]),
            is_active=bool(payload["is_active"]),
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
