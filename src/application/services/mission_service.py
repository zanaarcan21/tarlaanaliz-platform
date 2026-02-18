# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Mission command models are explicit and validated at the application boundary.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .mission_lifecycle_manager import Mission, MissionLifecycleManager


class MissionRepository(Protocol):
    def create(self, mission: Mission) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


@dataclass(frozen=True, slots=True)
class CreateMissionRequest:
    mission_id: str
    field_id: str


class MissionService:
    def __init__(self, repo: MissionRepository, lifecycle: MissionLifecycleManager, bus: EventBus) -> None:
        self._repo = repo
        self._lifecycle = lifecycle
        self._bus = bus

    def create_mission(self, *, req: CreateMissionRequest, correlation_id: str) -> Mission:
        mission = Mission(mission_id=req.mission_id, field_id=req.field_id, status="draft")
        self._repo.create(mission)
        self._bus.publish("mission.created", {"mission_id": mission.mission_id}, correlation_id=correlation_id)
        return mission

    def schedule_mission(self, *, mission_id: str, scheduled_ts_ms: int, correlation_id: str) -> Mission:
        return self._lifecycle.transition(
            mission_id=mission_id,
            to_status="scheduled",
            scheduled_ts_ms=scheduled_ts_ms,
            correlation_id=correlation_id,
        )

    def assign_mission(self, *, mission_id: str, pilot_id: str, correlation_id: str) -> Mission:
        return self._lifecycle.transition(
            mission_id=mission_id,
            to_status="assigned",
            pilot_id=pilot_id,
            correlation_id=correlation_id,
        )
