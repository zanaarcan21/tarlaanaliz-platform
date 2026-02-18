# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application handler for expert-review-completed events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.core.domain.events.expert_review_events import ExpertReviewCompleted


class ExpertReviewProjectionPort(Protocol):
    """Projection update port for completed expert reviews."""

    async def mark_completed(self, review_id: str, decision: str) -> None: ...


class TrainingFeedbackPort(Protocol):
    """Port to export completed review as feedback input."""

    async def enqueue_feedback(self, review_id: str, decision: str) -> None: ...


@dataclass(slots=True)
class ExpertReviewCompletedHandler:
    """Updates projections and training queue when expert review is done."""

    projection_port: ExpertReviewProjectionPort
    training_feedback_port: TrainingFeedbackPort

    # KR-081: event-shape-first handling through typed event.
    async def handle(self, event: ExpertReviewCompleted) -> None:
        review_id = str(event.review_id)
        await self.projection_port.mark_completed(review_id=review_id, decision=event.decision)
        await self.training_feedback_port.enqueue_feedback(review_id=review_id, decision=event.decision)
