# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for contract-first payload mapping."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class MissionAssetDTO:
    asset_type: str
    asset_uri: str
    checksum_sha256: str


@dataclass(frozen=True, slots=True)
class MissionDTO:
    mission_id: str
    field_id: str
    pilot_id: str
    crop_type: str
    status: str
    scheduled_date: date
    assigned_area_m2: float
    delivered_area_m2: float | None
    assets: tuple[MissionAssetDTO, ...]
    created_at: datetime
    updated_at: datetime

    # KR-015: explicit planning capacity related fields (date + area) included in read-model.
    # KR-016: mission_id exposed as canonical mission reference.
    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "field_id": self.field_id,
            "pilot_id": self.pilot_id,
            "crop_type": self.crop_type,
            "status": self.status,
            "scheduled_date": self.scheduled_date.isoformat(),
            "assigned_area_m2": self.assigned_area_m2,
            "delivered_area_m2": self.delivered_area_m2,
            "assets": [
                {
                    "asset_type": asset.asset_type,
                    "asset_uri": asset.asset_uri,
                    "checksum_sha256": asset.checksum_sha256,
                }
                for asset in self.assets
            ],
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MissionDTO:
        return cls(
            mission_id=str(payload["mission_id"]),
            field_id=str(payload["field_id"]),
            pilot_id=str(payload["pilot_id"]),
            crop_type=str(payload["crop_type"]),
            status=str(payload["status"]),
            scheduled_date=_parse_date(payload["scheduled_date"]),
            assigned_area_m2=float(payload["assigned_area_m2"]),
            delivered_area_m2=(
                None if payload.get("delivered_area_m2") is None else float(payload["delivered_area_m2"])
            ),
            assets=tuple(
                MissionAssetDTO(
                    asset_type=str(item["asset_type"]),
                    asset_uri=str(item["asset_uri"]),
                    checksum_sha256=str(item["checksum_sha256"]),
                )
                for item in payload.get("assets", [])
            ),
            created_at=_parse_datetime(payload["created_at"]),
            updated_at=_parse_datetime(payload["updated_at"]),
        )


def _to_utc_iso(value: datetime) -> str:
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_date(raw: Any) -> date:
    if isinstance(raw, date) and not isinstance(raw, datetime):
        return raw
    return date.fromisoformat(str(raw))


def _parse_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
