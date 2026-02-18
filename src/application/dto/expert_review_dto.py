# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for contract-first payload mapping."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class ExpertReviewDTO:
    review_id: str
    analysis_id: str
    mission_id: str
    expert_id: str
    status: str
    score: float | None
    notes: str | None
    created_at: datetime
    submitted_at: datetime | None
    correlation_id: str | None

    # KR-081: explicit schema-compatible review payload.
    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "analysis_id": self.analysis_id,
            "mission_id": self.mission_id,
            "expert_id": self.expert_id,
            "status": self.status,
            "score": self.score,
            "notes": self.notes,
            "created_at": _to_utc_iso(self.created_at),
            "submitted_at": _optional_dt(self.submitted_at),
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ExpertReviewDTO:
        return cls(
            review_id=str(payload["review_id"]),
            analysis_id=str(payload["analysis_id"]),
            mission_id=str(payload["mission_id"]),
            expert_id=str(payload["expert_id"]),
            status=str(payload["status"]),
            score=None if payload.get("score") is None else float(payload["score"]),
            notes=None if payload.get("notes") is None else str(payload["notes"]),
            created_at=_parse_datetime(payload["created_at"]),
            submitted_at=_parse_optional_datetime(payload.get("submitted_at")),
            correlation_id=None if payload.get("correlation_id") is None else str(payload["correlation_id"]),
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
    parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
