# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Capacity policy and estimations are centralized for scheduling inputs.

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlanningCapacityPolicy:
    min_daily_capacity_donum: int = 2500
    max_daily_capacity_donum: int = 3000
    work_days_max: int = 6
    effort_per_donum: float = 1.0


@dataclass(frozen=True, slots=True)
class CapacityEstimate:
    donum: float
    effort_units: float
    daily_capacity_donum: int
    estimated_days: float


def donum_to_effort(donum: float, *, policy: PlanningCapacityPolicy | None = None) -> float:
    p = policy or PlanningCapacityPolicy()
    return max(0.0, float(donum)) * p.effort_per_donum


def estimate_daily_capacity(*, requested: int, policy: PlanningCapacityPolicy | None = None) -> int:
    p = policy or PlanningCapacityPolicy()
    return max(p.min_daily_capacity_donum, min(p.max_daily_capacity_donum, int(requested)))


def estimate_days_for_area(
    donum: float,
    *,
    daily_capacity_donum: int,
    policy: PlanningCapacityPolicy | None = None,
) -> float:
    capacity = estimate_daily_capacity(requested=daily_capacity_donum, policy=policy)
    if capacity <= 0:
        return float("inf")
    return float(donum) / float(capacity)


def estimate_capacity(
    donum: float,
    *,
    daily_capacity_donum: int,
    policy: PlanningCapacityPolicy | None = None,
) -> CapacityEstimate:
    effort = donum_to_effort(donum, policy=policy)
    capacity = estimate_daily_capacity(requested=daily_capacity_donum, policy=policy)
    days = estimate_days_for_area(donum, daily_capacity_donum=capacity, policy=policy)
    return CapacityEstimate(donum=float(donum), effort_units=effort, daily_capacity_donum=capacity, estimated_days=days)
