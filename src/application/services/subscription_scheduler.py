# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Seasonal slot generation uses deterministic scheduling intervals.

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeasonPlan:
    subscription_id: str
    season_year: int
    mission_slots_ts_ms: tuple[int, ...]


class SubscriptionScheduler:
    def __init__(self, *, slot_interval_days: int = 14) -> None:
        self._interval_days = int(slot_interval_days)

    def build_season_plan(
        self,
        *,
        subscription_id: str,
        season_year: int,
        season_start_ts_ms: int,
        season_end_ts_ms: int,
        correlation_id: str,
    ) -> SeasonPlan:
        _ = correlation_id
        interval_ms = self._interval_days * 24 * 60 * 60 * 1000
        slots: list[int] = []
        cursor = int(season_start_ts_ms)
        while cursor <= int(season_end_ts_ms):
            slots.append(cursor)
            cursor += interval_ms
        return SeasonPlan(subscription_id=subscription_id, season_year=season_year, mission_slots_ts_ms=tuple(slots))
