# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/expert_schemas.py
# DESC: Expert request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class ExpertRole(str, Enum):
    expert = "expert"
    lead_expert = "lead_expert"
    admin = "admin"


class ExpertLevel(str, Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"
    principal = "principal"


class ExpertCreateRequest(SchemaBase):
    # KR-081: explicit contract for expert onboarding at API boundary.
    display_name: str = Field(min_length=2, max_length=80)
    role: ExpertRole = ExpertRole.expert
    level: ExpertLevel = ExpertLevel.junior
    specialties: list[str] = Field(default_factory=list, max_length=30)


class ExpertUpdateRequest(SchemaBase):
    display_name: str | None = Field(default=None, min_length=2, max_length=80)
    role: ExpertRole | None = None
    level: ExpertLevel | None = None
    specialties: list[str] | None = Field(default=None, max_length=30)
    active: bool | None = None


class ExpertProfileResponse(SchemaBase):
    id: UUID
    display_name: str
    role: ExpertRole
    level: ExpertLevel
    specialties: list[str] = Field(default_factory=list)
    active: bool
    created_at: datetime
    updated_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class PaginationMeta(SchemaBase):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class ExpertListResponse(SchemaBase):
    items: list[ExpertProfileResponse] = Field(default_factory=list)
    pagination: PaginationMeta
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
