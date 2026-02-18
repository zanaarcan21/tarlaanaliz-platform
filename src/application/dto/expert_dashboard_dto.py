# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application DTOs for expert dashboard responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ExpertDashboardStatsDTO:
    pending_reviews: int
    completed_reviews: int
    avg_turnaround_minutes: float | None


@dataclass(frozen=True, slots=True)
class ExpertDashboardDTO:
    """Composite dashboard DTO for expert UI consumption."""

    expert_id: str
    stats: ExpertDashboardStatsDTO
    queue_items: tuple[str, ...]
    priority_mission_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "expert_id": self.expert_id,
            "stats": {
                "pending_reviews": self.stats.pending_reviews,
                "completed_reviews": self.stats.completed_reviews,
                "avg_turnaround_minutes": self.stats.avg_turnaround_minutes,
            },
            "queue_items": list(self.queue_items),
            "priority_mission_ids": list(self.priority_mission_ids),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExpertDashboardDTO":
        stats = payload["stats"]
        return cls(
            expert_id=str(payload["expert_id"]),
            stats=ExpertDashboardStatsDTO(
                pending_reviews=int(stats["pending_reviews"]),
                completed_reviews=int(stats["completed_reviews"]),
                avg_turnaround_minutes=(
                    None
                    if stats.get("avg_turnaround_minutes") is None
                    else float(stats["avg_turnaround_minutes"])
                ),
            ),
            queue_items=tuple(str(v) for v in payload.get("queue_items", [])),
            priority_mission_ids=tuple(str(v) for v in payload.get("priority_mission_ids", [])),
        )
