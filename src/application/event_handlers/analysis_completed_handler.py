# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Application handler for analysis-completed events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from src.core.domain.events.analysis_events import AnalysisCompleted
from src.core.domain.events.expert_review_events import ExpertReviewRequested
from src.core.domain.value_objects.ai_confidence import AIConfidence


class AnalysisResultSink(Protocol):
    """Port for persisting analysis-completed payloads."""

    async def persist_completed_event(self, event: AnalysisCompleted) -> None: ...


class ExpertReviewTrigger(Protocol):
    """Port for creating a review request on low-confidence results."""

    async def request_review(self, event: ExpertReviewRequested) -> None: ...


@dataclass(slots=True)
class AnalysisCompletedHandler:
    """Persists analysis completion and optionally requests expert review."""

    result_sink: AnalysisResultSink
    review_trigger: ExpertReviewTrigger
    # KR-019: domain-level expert review threshold must match AI confidence policy.
    confidence_threshold: float = AIConfidence.DEFAULT_EXPERT_REVIEW_THRESHOLD

    # KR-081: Event payload is handled as contract-defined shape.
    # KR-018: Handler is only for completed analysis events after calibration gate.
    async def handle(self, event: AnalysisCompleted) -> None:
        await self.result_sink.persist_completed_event(event)

        if event.confidence_score >= self.confidence_threshold:
            return

        # KR-081: emit typed domain event for review request.
        review_event = ExpertReviewRequested(
            analysis_job_id=event.analysis_job_id,
            field_id=event.field_id,
            confidence_score=event.confidence_score,
            occurred_at=datetime.now(timezone.utc),
        )
        await self.review_trigger.request_review(review_event)
