# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-019: Expert review threshold must follow AI confidence policy.

from __future__ import annotations

import asyncio

from src.application.event_handlers.analysis_completed_handler import AnalysisCompletedHandler
from src.core.domain.events.analysis_events import AnalysisCompleted
from src.core.domain.value_objects.ai_confidence import AIConfidence


class _InMemoryResultSink:
    def __init__(self) -> None:
        self.events: list[AnalysisCompleted] = []

    async def persist_completed_event(self, event: AnalysisCompleted) -> None:
        self.events.append(event)


class _InMemoryReviewTrigger:
    def __init__(self) -> None:
        self.events: list[object] = []

    async def request_review(self, event: object) -> None:
        self.events.append(event)


def test_handler_uses_kr019_default_threshold() -> None:
    handler = AnalysisCompletedHandler(
        result_sink=_InMemoryResultSink(),
        review_trigger=_InMemoryReviewTrigger(),
    )

    assert handler.confidence_threshold == AIConfidence.DEFAULT_EXPERT_REVIEW_THRESHOLD


def test_handler_requests_review_below_default_threshold() -> None:
    sink = _InMemoryResultSink()
    trigger = _InMemoryReviewTrigger()
    handler = AnalysisCompletedHandler(result_sink=sink, review_trigger=trigger)

    event = AnalysisCompleted(confidence_score=0.70)
    asyncio.run(handler.handle(event))

    assert len(sink.events) == 1
    assert len(trigger.events) == 1
