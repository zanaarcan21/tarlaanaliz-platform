# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Mission lifecycle transitions follow explicit policy guards.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class Mission:
    mission_id: str
    field_id: str
    status: str
    pilot_id: str | None = None
    scheduled_ts_ms: int | None = None


class MissionRepository(Protocol):
    def get(self, mission_id: str) -> Mission | None: ...

    def update(self, mission: Mission) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class MissionLifecycleManager:
    def __init__(self, repo: MissionRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def transition(self, *, mission_id: str, to_status: str, correlation_id: str, **patch: Any) -> Mission:
        mission = self._repo.get(mission_id)
        if mission is None:
            raise ValueError("mission not found")

        allowed: dict[str, set[str]] = {
            "draft": {"scheduled", "cancelled"},
            "scheduled": {"assigned", "cancelled"},
            "assigned": {"flown", "cancelled"},
            "flown": {"uploaded"},
            "uploaded": {"analyzing"},
            "analyzing": {"completed"},
            "completed": set(),
            "cancelled": set(),
        }
        if to_status not in allowed.get(mission.status, set()):
            raise ValueError(f"invalid transition {mission.status} -> {to_status}")

        updated = Mission(
            mission_id=mission.mission_id,
            field_id=mission.field_id,
            status=to_status,
            pilot_id=patch.get("pilot_id", mission.pilot_id),
            scheduled_ts_ms=patch.get("scheduled_ts_ms", mission.scheduled_ts_ms),
        )
        self._repo.update(updated)
        self._bus.publish(
            "mission.status_changed",
            {"mission_id": mission_id, "from": mission.status, "to": to_status},
            correlation_id=correlation_id,
        )
        return updated
