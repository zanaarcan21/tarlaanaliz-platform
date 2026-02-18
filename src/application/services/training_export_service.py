# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-071: Training export flow only emits outbound events to integration boundaries.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class TrainingExportRequest:
    export_id: str
    dataset_id: str
    format: str


class TrainingExportStore(Protocol):
    def create_export_job(self, req: TrainingExportRequest) -> None: ...

    def mark_ready(self, export_id: str, *, uri: str) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class TrainingExportService:
    def __init__(self, store: TrainingExportStore, bus: EventBus) -> None:
        self._store = store
        self._bus = bus

    def request_export(self, *, req: TrainingExportRequest, correlation_id: str) -> None:
        self._store.create_export_job(req)
        self._bus.publish(
            "training_export.requested",
            {"export_id": req.export_id, "dataset_id": req.dataset_id, "format": req.format},
            correlation_id=correlation_id,
        )
