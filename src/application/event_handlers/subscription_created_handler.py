# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application handler for subscription-created events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import uuid
from typing import Protocol

from src.core.domain.events.subscription_events import MissionScheduled, SubscriptionCreated


class MissionScheduleSink(Protocol):
    """Port to persist scheduled mission rows."""

    async def create_scheduled_mission(
        self,
        *,
        subscription_id: str,
        field_id: str,
        scheduled_date: date,
    ) -> str: ...


class MissionSchedulePublisher(Protocol):
    """Port to publish MissionScheduled event."""

    async def publish_mission_scheduled(self, event: MissionScheduled) -> None: ...


@dataclass(slots=True)
class SubscriptionCreatedHandler:
    """Expands subscription into future mission schedule entries."""

    schedule_sink: MissionScheduleSink
    publisher: MissionSchedulePublisher

    # KR-015: schedule expansion follows interval and total analyses.
    # KR-081: event-first contract handling.
    async def handle(self, event: SubscriptionCreated) -> tuple[str, ...]:
        if event.start_date is None:
            return ()

        scheduled_missions: list[str] = []
        step_days = max(1, event.interval_days)

        for index in range(max(0, event.total_analyses)):
            run_date = event.start_date + timedelta(days=index * step_days)
            if event.end_date and run_date > event.end_date:
                break

            mission_id = await self.schedule_sink.create_scheduled_mission(
                subscription_id=str(event.subscription_id),
                field_id=str(event.field_id),
                scheduled_date=run_date,
            )
            scheduled_missions.append(mission_id)

            await self.publisher.publish_mission_scheduled(
                MissionScheduled(
                    subscription_id=event.subscription_id,
                    mission_id=uuid.UUID(mission_id),
                    scheduled_date=run_date,
                )
            )

        return tuple(scheduled_missions)
