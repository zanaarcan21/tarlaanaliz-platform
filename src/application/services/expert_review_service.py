# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Expert review orchestration consumes explicit contracts.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ExpertReview:
    review_id: str
    analysis_id: str
    expert_id: str
    status: str
    notes: str | None = None


class ExpertReviewRepository(Protocol):
    def create(self, review: ExpertReview) -> None: ...

    def get(self, review_id: str) -> ExpertReview | None: ...

    def list_pending(self, *, limit: int) -> tuple[ExpertReview, ...]: ...

    def update(self, review: ExpertReview) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class ExpertReviewService:
    def __init__(self, repo: ExpertReviewRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def create_review(self, *, review: ExpertReview, correlation_id: str) -> None:
        self._repo.create(review)
        self._bus.publish(
            "expert_review.created",
            {"review_id": review.review_id, "analysis_id": review.analysis_id, "expert_id": review.expert_id},
            correlation_id=correlation_id,
        )

    def submit_review(self, *, review_id: str, notes: str, correlation_id: str) -> ExpertReview:
        review = self._repo.get(review_id)
        if review is None:
            raise ValueError("expert review not found")
        updated = ExpertReview(
            review_id=review.review_id,
            analysis_id=review.analysis_id,
            expert_id=review.expert_id,
            status="completed",
            notes=notes,
        )
        self._repo.update(updated)
        self._bus.publish(
            "expert_review.completed",
            {"review_id": updated.review_id, "analysis_id": updated.analysis_id, "expert_id": updated.expert_id},
            correlation_id=correlation_id,
        )
        return updated
