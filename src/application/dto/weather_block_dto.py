# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for weather block reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class WeatherBlockDTO:
    """Weather block/report DTO for weather-block endpoints."""

    weather_block_id: str
    mission_id: str
    field_id: str
    reported_by_user_id: str
    reason_code: str
    severity: str
    blocked_from: datetime
    blocked_until: datetime
    notes: str | None
    verification_status: str
    verified_by_user_id: str | None
    verified_at: datetime | None
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "weather_block_id": self.weather_block_id,
            "mission_id": self.mission_id,
            "field_id": self.field_id,
            "reported_by_user_id": self.reported_by_user_id,
            "reason_code": self.reason_code,
            "severity": self.severity,
            "blocked_from": _to_utc_iso(self.blocked_from),
            "blocked_until": _to_utc_iso(self.blocked_until),
            "notes": self.notes,
            "verification_status": self.verification_status,
            "verified_by_user_id": self.verified_by_user_id,
            "verified_at": _optional_dt(self.verified_at),
            "created_at": _to_utc_iso(self.created_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WeatherBlockDTO":
        return cls(
            weather_block_id=str(payload["weather_block_id"]),
            mission_id=str(payload["mission_id"]),
            field_id=str(payload["field_id"]),
            reported_by_user_id=str(payload["reported_by_user_id"]),
            reason_code=str(payload["reason_code"]),
            severity=str(payload["severity"]),
            blocked_from=_parse_datetime(payload["blocked_from"]),
            blocked_until=_parse_datetime(payload["blocked_until"]),
            notes=None if payload.get("notes") is None else str(payload["notes"]),
            verification_status=str(payload["verification_status"]),
            verified_by_user_id=(
                None if payload.get("verified_by_user_id") is None else str(payload["verified_by_user_id"])
            ),
            verified_at=_parse_optional_datetime(payload.get("verified_at")),
            created_at=_parse_datetime(payload["created_at"]),
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
    dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
