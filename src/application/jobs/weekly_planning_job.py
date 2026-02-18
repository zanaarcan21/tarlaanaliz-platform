# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Weekly planning application job orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


class WeeklyPlanner(Protocol):
    """Port to compute and persist weekly schedule."""

    async def plan_week(self, *, week_start: date, correlation_id: str) -> int: ...


class AuditWriter(Protocol):
    """Port to append planning audit entries."""

    async def append_job_log(
        self,
        *,
        correlation_id: str,
        outcome: str,
        affected_count: int,
    ) -> None: ...


@dataclass(slots=True)
class WeeklyPlanningJob:
    """Runs weekly planning and emits audit side effect."""

    planner: WeeklyPlanner
    audit_writer: AuditWriter

    # KR-015: weekly capacity/scheduling automation entry point.
    async def run(self, *, week_start: date, correlation_id: str) -> int:
        planned_count = await self.planner.plan_week(
            week_start=week_start,
            correlation_id=correlation_id,
        )

        await self.audit_writer.append_job_log(
            correlation_id=correlation_id,
            outcome="SUCCESS",
            affected_count=planned_count,
        )
        return planned_count
