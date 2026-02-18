# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for mission payloads (contract-mappable)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class MissionAssetDTO:
    """Mission output or source asset reference."""

    asset_type: str
    uri: str
    checksum: str | None


@dataclass(frozen=True, slots=True)
class MissionDTO:
    """Mission lifecycle DTO for API schema mapping."""

    mission_id: str
    field_id: str
    pilot_id: str | None
    subscription_id: str | None
    mission_code: str
    status: str
    scheduled_start_at: datetime
    scheduled_end_at: datetime | None
    flown_at: datetime | None
    kmz_uri: str | None
    area_donum: float
    notes: str | None
    outputs: tuple[MissionAssetDTO, ...]
    created_at: datetime
    updated_at: datetime

    # KR-016: mission code and output naming must remain contract-aligned.
    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["scheduled_start_at"] = _to_utc_iso(self.scheduled_start_at)
        data["scheduled_end_at"] = _optional_dt(self.scheduled_end_at)
        data["flown_at"] = _optional_dt(self.flown_at)
        data["created_at"] = _to_utc_iso(self.created_at)
        data["updated_at"] = _to_utc_iso(self.updated_at)
        return data

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MissionDTO":
        return cls(
            mission_id=str(payload["mission_id"]),
            field_id=str(payload["field_id"]),
            pilot_id=_to_optional_str(payload.get("pilot_id")),
            subscription_id=_to_optional_str(payload.get("subscription_id")),
            mission_code=str(payload["mission_code"]),
            status=str(payload["status"]),
            scheduled_start_at=_parse_datetime(payload["scheduled_start_at"]),
            scheduled_end_at=_parse_optional_datetime(payload.get("scheduled_end_at")),
            flown_at=_parse_optional_datetime(payload.get("flown_at")),
            kmz_uri=_to_optional_str(payload.get("kmz_uri")),
            area_donum=float(payload["area_donum"]),
            notes=_to_optional_str(payload.get("notes")),
            outputs=tuple(
                MissionAssetDTO(
                    asset_type=str(item["asset_type"]),
                    uri=str(item["uri"]),
                    checksum=_to_optional_str(item.get("checksum")),
                )
                for item in payload.get("outputs", [])
            ),
            created_at=_parse_datetime(payload["created_at"]),
            updated_at=_parse_datetime(payload["updated_at"]),
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
