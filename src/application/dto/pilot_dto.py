# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for contract-first payload mapping."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class PilotDTO:
    pilot_id: str
    display_name: str
    masked_phone: str
    territory_id: str
    work_days: tuple[int, ...]
    daily_capacity_donum: int
    system_seed_quota_donum: int
    reliability_score: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        # KR-015: work_days <= 6 and explicit capacity constraints.
        if len(self.work_days) > 6:
            raise ValueError("work_days cannot exceed 6")
        if self.daily_capacity_donum <= 0:
            raise ValueError("daily_capacity_donum must be > 0")
        if self.system_seed_quota_donum < 0:
            raise ValueError("system_seed_quota_donum must be >= 0")
        if self.system_seed_quota_donum > self.daily_capacity_donum:
            raise ValueError("system_seed_quota_donum cannot exceed daily_capacity_donum")

    # KR-015: capacity and work day constraints are explicit for planning reads.
    def to_dict(self) -> dict[str, Any]:
        return {
            "pilot_id": self.pilot_id,
            "display_name": self.display_name,
            "masked_phone": self.masked_phone,
            "territory_id": self.territory_id,
            "work_days": list(self.work_days),
            "daily_capacity_donum": self.daily_capacity_donum,
            "system_seed_quota_donum": self.system_seed_quota_donum,
            "reliability_score": self.reliability_score,
            "is_active": self.is_active,
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> PilotDTO:
        return cls(
            pilot_id=str(payload["pilot_id"]),
            display_name=str(payload["display_name"]),
            masked_phone=str(payload["masked_phone"]),
            territory_id=str(payload["territory_id"]),
            work_days=tuple(int(day) for day in payload.get("work_days", [])),
            daily_capacity_donum=int(payload["daily_capacity_donum"]),
            system_seed_quota_donum=int(payload["system_seed_quota_donum"]),
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
    parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
