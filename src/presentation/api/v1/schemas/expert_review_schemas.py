# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/expert_review_schemas.py
# DESC: Expert review request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class ExpertReviewDecision(str, Enum):
    approve = "approve"
    reject = "reject"
    needs_more_data = "needs_more_data"


class ExpertReviewCreateRequest(SchemaBase):
    # KR-081: review submission contract is explicit at API boundary.
    analysis_job_id: UUID | None = None
    mission_id: UUID | None = None
    decision: ExpertReviewDecision
    notes: str | None = Field(default=None, max_length=1000)
    labels: list[str] = Field(default_factory=list, max_length=25)

    @model_validator(mode="after")
    def validate_target(self) -> ExpertReviewCreateRequest:
        if not self.analysis_job_id and not self.mission_id:
            raise ValueError("Either analysis_job_id or mission_id must be provided")
        return self


class ExpertReviewUpdateRequest(SchemaBase):
    decision: ExpertReviewDecision | None = None
    notes: str | None = Field(default=None, max_length=1000)
    labels: list[str] | None = Field(default=None, max_length=25)


class ExpertReviewResponse(SchemaBase):
    id: UUID
    analysis_job_id: UUID | None = None
    mission_id: UUID | None = None
    expert_id: UUID
    decision: ExpertReviewDecision
    notes: str | None = None
    labels: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class PaginationMeta(SchemaBase):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class ExpertReviewListResponse(SchemaBase):
    items: list[ExpertReviewResponse] = Field(default_factory=list)
    pagination: PaginationMeta
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
