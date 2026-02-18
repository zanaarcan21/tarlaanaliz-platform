# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for field payloads (contract-mappable)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, slots=True)
class FieldCoordinatesDTO:
    """Geo point for field geometry."""

    lat: float
    lon: float


@dataclass(frozen=True, slots=True)
class FieldDTO:
    """Field data transfer model for application/presentation mapping."""

    field_id: str
    owner_user_id: str
    name: str
    city: str | None
    district: str | None
    area_donum: Decimal
    parcel_reference: str | None
    boundary: tuple[FieldCoordinatesDTO, ...]
    crop_type: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["area_donum"] = str(self.area_donum)
        data["created_at"] = _to_utc_iso(self.created_at)
        data["updated_at"] = _to_utc_iso(self.updated_at)
        return data

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "FieldDTO":
        return cls(
            field_id=str(payload["field_id"]),
            owner_user_id=str(payload["owner_user_id"]),
            name=str(payload["name"]),
            city=_to_optional_str(payload.get("city")),
            district=_to_optional_str(payload.get("district")),
            area_donum=Decimal(str(payload["area_donum"])),
            parcel_reference=_to_optional_str(payload.get("parcel_reference")),
            boundary=tuple(
                FieldCoordinatesDTO(lat=float(p["lat"]), lon=float(p["lon"]))
                for p in payload.get("boundary", [])
            ),
            crop_type=_to_optional_str(payload.get("crop_type")),
            status=str(payload["status"]),
            created_at=_parse_datetime(payload["created_at"]),
            updated_at=_parse_datetime(payload["updated_at"]),
        )


def _to_optional_str(value: Any) -> str | None:
    return None if value is None else str(value)


def _to_utc_iso(value: datetime) -> str:
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    text = str(raw)
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
