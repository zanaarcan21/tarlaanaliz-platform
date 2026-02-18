# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-015: Pilot scheduling and reassignment journey.

from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timezone

import pytest

from src.core.domain.entities.pilot import Pilot
from src.core.domain.services.capacity_manager import CapacityManager, PilotAssignment, PilotCapacity
from src.core.domain.services.reschedule_service import RescheduleService
from src.core.domain.value_objects.pilot_schedule import PilotSchedule

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        os.getenv("RUN_E2E") != "1" and os.getenv("E2E") != "1",
        reason="E2E tests disabled. Set RUN_E2E=1 or E2E=1.",
    ),
]


class _AlwaysAvailablePilot:
    def is_available(self, pilot_id: str, date_iso: str) -> bool:
        return True


class _Subscription:
    id = "sub-1"
    reschedule_tokens_remaining = 2


class _Mission:
    id = "mission-1"
    scheduled_date = "2026-01-10"
    schedule_window_start = "2026-01-01"
    schedule_window_end = "2026-01-31"
    assigned_pilot_id = "pilot-1"


def test_pilot_journey_capacity_and_reschedule_rules() -> None:
    # KR-015: work_days <= 6 & capacity 2500-3000
    with pytest.raises(ValueError, match="work_days cannot exceed 6"):
        Pilot(
            pilot_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            province="Konya",
            district="Selcuklu",
            full_name="Pilot Dummy",
            phone_number="+905550000999",
            drone_model="DJI Mavic 3M",
            drone_serial_number="SN-001",
            work_days=[0, 1, 2, 3, 4, 5, 6],
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

    schedule = PilotSchedule(work_days=frozenset({0, 1, 2, 3, 4, 5}), daily_capacity_donum=2800)
    schedule.validate()
    assert schedule.pull_quota_donum() == 1300

    manager = CapacityManager()
    capacity = PilotCapacity(
        pilot_id=uuid.uuid4(),
        work_days=frozenset({0, 1, 2, 3, 4, 5}),
        daily_capacity=2,
        province_code="42",
    )
    today = date(2026, 1, 5)
    assignments = [
        PilotAssignment(pilot_id=capacity.pilot_id, mission_id=uuid.uuid4(), scheduled_date=today),
        PilotAssignment(pilot_id=capacity.pilot_id, mission_id=uuid.uuid4(), scheduled_date=today),
    ]

    availability = manager.check_availability(capacity, today, assignments)
    assert availability.is_available is False

    reschedule_result = RescheduleService(_AlwaysAvailablePilot()).reschedule(
        subscription=_Subscription(),
        mission=_Mission(),
        new_date_iso="2026-01-20",
    )
    assert reschedule_result.ok is True
    assert reschedule_result.token_remaining == 1
