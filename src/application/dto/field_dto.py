# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for contract-first payload mapping."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class FieldCoordinatesDTO:
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True)
class FieldDTO:
    field_id: str
    owner_ref: str
    parcel_ref: str
    city_code: str
    district_code: str
    village_name: str
    area_m2: float
    crop_types: tuple[str, ...]
    centroid: FieldCoordinatesDTO
    created_at: datetime
    updated_at: datetime

    # KR-081: predictable API contract shape.
    def to_dict(self) -> dict[str, Any]:
        return {
            "field_id": self.field_id,
            "owner_ref": self.owner_ref,
            "parcel_ref": self.parcel_ref,
            "city_code": self.city_code,
            "district_code": self.district_code,
            "village_name": self.village_name,
            "area_m2": self.area_m2,
            "crop_types": list(self.crop_types),
            "centroid": {"latitude": self.centroid.latitude, "longitude": self.centroid.longitude},
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FieldDTO:
        raw_centroid = payload["centroid"]
        return cls(
            field_id=str(payload["field_id"]),
            owner_ref=str(payload["owner_ref"]),
            parcel_ref=str(payload["parcel_ref"]),
            city_code=str(payload["city_code"]),
            district_code=str(payload["district_code"]),
            village_name=str(payload["village_name"]),
            area_m2=float(payload["area_m2"]),
            crop_types=tuple(str(item) for item in payload.get("crop_types", [])),
            centroid=FieldCoordinatesDTO(
                latitude=float(raw_centroid["latitude"]),
                longitude=float(raw_centroid["longitude"]),
            ),
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
