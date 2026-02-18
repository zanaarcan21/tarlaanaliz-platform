# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Pricebook snapshots use typed contracts at application boundaries.

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PriceSnapshot:
    snapshot_id: str
    currency: str
    valid_from_ts_ms: int
    items: dict[str, int]


class PricebookRepository(Protocol):
    def upsert_snapshot(self, snap: PriceSnapshot) -> None: ...

    def get_active_snapshot(self, *, at_ts_ms: int) -> PriceSnapshot | None: ...

    def list_snapshots(self, *, limit: int) -> tuple[PriceSnapshot, ...]: ...


class PricebookService:
    def __init__(self, repo: PricebookRepository) -> None:
        self._repo = repo

    def publish_snapshot(self, *, snap: PriceSnapshot, correlation_id: str) -> None:
        _ = correlation_id
        self._repo.upsert_snapshot(snap)

    def get_active(self, *, at_ts_ms: int) -> PriceSnapshot | None:
        return self._repo.get_active_snapshot(at_ts_ms=at_ts_ms)

    def list_recent(self, *, limit: int = 50) -> tuple[PriceSnapshot, ...]:
        return self._repo.list_snapshots(limit=limit)
