# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application handler for mission lifecycle events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.core.domain.events.mission_events import MissionCancelled, MissionCompleted, MissionReplanQueued


class MissionLifecycleStore(Protocol):
    """Port to persist mission lifecycle side-effects."""

    async def mark_cancelled(self, mission_id: str, reason: str) -> None: ...
    async def mark_completed(self, mission_id: str) -> None: ...


class ReplanQueuePort(Protocol):
    """Port to enqueue mission replan requests."""

    async def enqueue(self, mission_id: str, reason: str) -> None: ...


@dataclass(slots=True)
class MissionLifecycleHandler:
    """Handles mission cancellation/completion projections."""

    lifecycle_store: MissionLifecycleStore
    replan_queue: ReplanQueuePort

    async def handle_cancelled(self, event: MissionCancelled) -> None:
        mission_id = str(event.mission_id)
        await self.lifecycle_store.mark_cancelled(mission_id=mission_id, reason=event.cancel_reason)

        # KR-015: cancelled missions should be moved to replan flow.
        if event.cancel_reason in {"weather_block", "pilot_notice", "admin_override"}:
            await self.replan_queue.enqueue(mission_id=mission_id, reason=event.cancel_reason.upper())

    async def handle_replan_queued(self, event: MissionReplanQueued) -> None:
        await self.replan_queue.enqueue(
            mission_id=str(event.mission_id),
            reason=event.replan_reason,
        )

    async def handle_completed(self, event: MissionCompleted) -> None:
        await self.lifecycle_store.mark_completed(mission_id=str(event.mission_id))
