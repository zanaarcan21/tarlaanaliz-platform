# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-015: Weather-block flow triggers replan-ready events.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class WeatherBlockReport:
    report_id: str
    mission_id: str
    pilot_id: str
    ts_ms: int
    reason: str
    evidence_uri: str | None = None


class WeatherBlockRepository(Protocol):
    def create(self, report: WeatherBlockReport) -> None: ...

    def mark_verified(self, report_id: str, *, verified_by: str) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class WeatherBlockService:
    def __init__(self, repo: WeatherBlockRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def report(self, *, report: WeatherBlockReport, correlation_id: str) -> None:
        self._repo.create(report)
        self._bus.publish(
            "weather_block.reported",
            {"report_id": report.report_id, "mission_id": report.mission_id},
            correlation_id=correlation_id,
        )
