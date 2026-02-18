# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-071: Feedback flow is one-way into platform persistence and outbound events.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class TrainingFeedback:
    feedback_id: str
    dataset_id: str
    label_issue: str
    note: str


class TrainingFeedbackRepository(Protocol):
    def append(self, feedback: TrainingFeedback) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class TrainingFeedbackService:
    def __init__(self, repo: TrainingFeedbackRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def submit(self, *, feedback: TrainingFeedback, correlation_id: str) -> None:
        self._repo.append(feedback)
        self._bus.publish(
            "training_feedback.submitted",
            {
                "feedback_id": feedback.feedback_id,
                "dataset_id": feedback.dataset_id,
                "label_issue": feedback.label_issue,
            },
            correlation_id=correlation_id,
        )
