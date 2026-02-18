# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/training_feedback_schemas.py
# DESC: Training feedback request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class FeedbackLabel(str, Enum):
    healthy = "healthy"
    stressed = "stressed"
    diseased = "diseased"
    weed = "weed"
    uncertain = "uncertain"


class FeedbackType(str, Enum):
    confirm = "confirm"
    correction = "correction"
    reject = "reject"


class TrainingFeedbackCreateRequest(SchemaBase):
    # KR-071/KR-081: feedback payload is constrained and one-way consumable contract.
    model_id: str = Field(min_length=2, max_length=128)
    model_version: str = Field(min_length=1, max_length=64)
    sample_id: UUID
    label: FeedbackLabel
    feedback: FeedbackType
    confidence: float = Field(ge=0, le=1)
    notes: str | None = Field(default=None, max_length=1000)


class TrainingFeedbackResponse(SchemaBase):
    id: UUID
    model_id: str
    model_version: str
    sample_id: UUID
    label: FeedbackLabel
    feedback: FeedbackType
    confidence: float
    actor_id: str = Field(min_length=4, max_length=32)
    created_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
