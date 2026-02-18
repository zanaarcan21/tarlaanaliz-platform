# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/weather_block_schemas.py
# DESC: WeatherBlock request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class WeatherSource(str, Enum):
    meteorology_api = "meteorology_api"
    pilot_report = "pilot_report"
    manual = "manual"


class WeatherSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class WeatherBlockStatus(str, Enum):
    planned = "planned"
    active = "active"
    expired = "expired"
    cancelled = "cancelled"


class WeatherBlockCreateRequest(SchemaBase):
    # KR-015: operational planning reacts to these blocks in app/domain services.
    field_id: UUID | None = None
    region_id: UUID | None = None
    start_date: date
    end_date: date
    source: WeatherSource
    severity: WeatherSeverity
    notes: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_target_and_dates(self) -> WeatherBlockCreateRequest:
        if not self.field_id and not self.region_id:
            raise ValueError("Either field_id or region_id must be provided")
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        return self


class WeatherBlockResponse(SchemaBase):
    id: UUID
    field_id: UUID | None = None
    region_id: UUID | None = None
    start_date: date
    end_date: date
    source: WeatherSource
    severity: WeatherSeverity
    status: WeatherBlockStatus
    summary: str = Field(min_length=1, max_length=280)
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class PaginationMeta(SchemaBase):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class WeatherBlockListResponse(SchemaBase):
    items: list[WeatherBlockResponse] = Field(default_factory=list)
    pagination: PaginationMeta
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
