# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/mission_schemas.py
# DESC: Mission request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class SensorType(str, Enum):
    rgb = "RGB"
    multispectral = "MS"


class MissionStatus(str, Enum):
    planned = "planned"
    assigned = "assigned"
    flown = "flown"
    uploaded = "uploaded"
    calibrated = "calibrated"
    analyzed = "analyzed"
    failed = "failed"
    cancelled = "cancelled"


class FlightParamsSummary(SchemaBase):
    altitude_m: float = Field(gt=0, le=500)
    overlap_front_pct: int = Field(ge=10, le=95)
    overlap_side_pct: int = Field(ge=10, le=95)
    speed_mps: float = Field(gt=0, le=30)


class MissionCreateRequest(SchemaBase):
    # KR-015: capacity/planning constraints are domain-enforced, not schema-enforced.
    field_id: UUID
    planned_date: date
    sensor_type: SensorType
    flight_params: FlightParamsSummary
    pilot_id: UUID | None = None


class MissionUpdateRequest(SchemaBase):
    planned_date: date | None = None
    sensor_type: SensorType | None = None
    flight_params: FlightParamsSummary | None = None
    pilot_id: UUID | None = None
    status: MissionStatus | None = None


class MissionResponse(SchemaBase):
    id: UUID
    field_id: UUID
    pilot_id: UUID | None = None
    status: MissionStatus
    sensor_type: SensorType
    flight_params: FlightParamsSummary
    planned_date: date
    flown_at: datetime | None = None
    uploaded_at: datetime | None = None
    calibrated_at: datetime | None = None
    analyzed_at: datetime | None = None
    failed_at: datetime | None = None
    cancelled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class PaginationMeta(SchemaBase):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class MissionListFilter(SchemaBase):
    field_id: UUID | None = None
    pilot_id: UUID | None = None
    status: MissionStatus | None = None
    sensor_type: SensorType | None = None
    planned_date_from: date | None = None
    planned_date_to: date | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)

    @model_validator(mode="after")
    def validate_date_range(self) -> MissionListFilter:
        if self.planned_date_from and self.planned_date_to and self.planned_date_from > self.planned_date_to:
            raise ValueError("planned_date_from cannot be greater than planned_date_to")
        return self


class MissionListResponse(SchemaBase):
    items: list[MissionResponse] = Field(default_factory=list)
    pagination: PaginationMeta
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
