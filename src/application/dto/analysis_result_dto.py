# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for analysis result payloads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class AnalysisLayerDTO:
    """Single analysis layer summary."""

    layer_key: str
    value_type: str
    value_uri: str


@dataclass(frozen=True, slots=True)
class AnalysisResultDTO:
    """Analysis job output DTO."""

    analysis_id: str
    mission_id: str
    field_id: str
    status: str
    summary: str | None
    confidence_score: float | None
    layers: tuple[AnalysisLayerDTO, ...]
    created_at: datetime
    completed_at: datetime | None

    # KR-018: output belongs to calibrated mission flow.
    # KR-081: contract-first payload shape.
    def to_dict(self) -> dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "mission_id": self.mission_id,
            "field_id": self.field_id,
            "status": self.status,
            "summary": self.summary,
            "confidence_score": self.confidence_score,
            "layers": [
                {"layer_key": l.layer_key, "value_type": l.value_type, "value_uri": l.value_uri}
                for l in self.layers
            ],
            "created_at": _to_utc_iso(self.created_at),
            "completed_at": _optional_dt(self.completed_at),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AnalysisResultDTO":
        return cls(
            analysis_id=str(payload["analysis_id"]),
            mission_id=str(payload["mission_id"]),
            field_id=str(payload["field_id"]),
            status=str(payload["status"]),
            summary=_to_optional_str(payload.get("summary")),
            confidence_score=(
                None if payload.get("confidence_score") is None else float(payload["confidence_score"])
            ),
            layers=tuple(
                AnalysisLayerDTO(
                    layer_key=str(item["layer_key"]),
                    value_type=str(item["value_type"]),
                    value_uri=str(item["value_uri"]),
                )
                for item in payload.get("layers", [])
            ),
            created_at=_parse_datetime(payload["created_at"]),
            completed_at=_parse_optional_datetime(payload.get("completed_at")),
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
    dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
