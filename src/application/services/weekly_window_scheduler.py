# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Weekly windows are generated from deterministic slot rules.

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeeklyWindow:
    week_start_ts_ms: int
    week_end_ts_ms: int
    slots_ts_ms: tuple[int, ...]


class WeeklyWindowScheduler:
    def __init__(self, *, slot_per_day: int = 1) -> None:
        self._slot_per_day = max(1, int(slot_per_day))

    def build_week(self, *, week_start_ts_ms: int, correlation_id: str) -> WeeklyWindow:
        _ = correlation_id
        day_ms = 24 * 60 * 60 * 1000
        week_end = int(week_start_ts_ms) + 7 * day_ms - 1
        slots: list[int] = []
        for day in range(7):
            day_start = int(week_start_ts_ms) + day * day_ms
            for slot in range(self._slot_per_day):
                slots.append(day_start + (slot * (day_ms // self._slot_per_day)))
        return WeeklyWindow(week_start_ts_ms=int(week_start_ts_ms), week_end_ts_ms=week_end, slots_ts_ms=tuple(slots))
