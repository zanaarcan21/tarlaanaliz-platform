# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for expert user payloads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class ExpertDTO:
    """Expert profile DTO for assignment and review workflows."""

    expert_id: str
    display_name: str
    phone: str
    territory_ids: tuple[str, ...]
    skill_tags: tuple[str, ...]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "expert_id": self.expert_id,
            "display_name": self.display_name,
            "phone": self.phone,
            "territory_ids": list(self.territory_ids),
            "skill_tags": list(self.skill_tags),
            "is_active": self.is_active,
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExpertDTO":
        return cls(
            expert_id=str(payload["expert_id"]),
            display_name=str(payload["display_name"]),
            phone=str(payload["phone"]),
            territory_ids=tuple(str(v) for v in payload.get("territory_ids", [])),
            skill_tags=tuple(str(v) for v in payload.get("skill_tags", [])),
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
