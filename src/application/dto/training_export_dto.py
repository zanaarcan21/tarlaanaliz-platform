# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for training export payloads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class TrainingExportDTO:
    """Training export metadata DTO."""

    export_id: str
    generated_by_user_id: str
    status: str
    format: str
    dataset_uri: str | None
    sample_count: int
    created_at: datetime
    completed_at: datetime | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "export_id": self.export_id,
            "generated_by_user_id": self.generated_by_user_id,
            "status": self.status,
            "format": self.format,
            "dataset_uri": self.dataset_uri,
            "sample_count": self.sample_count,
            "created_at": _to_utc_iso(self.created_at),
            "completed_at": _optional_dt(self.completed_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TrainingExportDTO":
        return cls(
            export_id=str(payload["export_id"]),
            generated_by_user_id=str(payload["generated_by_user_id"]),
            status=str(payload["status"]),
            format=str(payload["format"]),
            dataset_uri=None if payload.get("dataset_uri") is None else str(payload["dataset_uri"]),
            sample_count=int(payload["sample_count"]),
            created_at=_parse_datetime(payload["created_at"]),
            completed_at=_parse_optional_datetime(payload.get("completed_at")),
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
