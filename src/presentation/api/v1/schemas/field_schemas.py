# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/field_schemas.py
# DESC: Field request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class CropType(str, Enum):
    wheat = "wheat"
    barley = "barley"
    corn = "corn"
    sunflower = "sunflower"
    cotton = "cotton"
    grape = "grape"
    olive = "olive"
    other = "other"


class GeoJSONPolygon(SchemaBase):
    type: Literal["Polygon"] = "Polygon"
    coordinates: list[list[list[float]]] = Field(min_length=1)


class GeoJSONMultiPolygon(SchemaBase):
    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: list[list[list[list[float]]]] = Field(min_length=1)


class ParcelReference(SchemaBase):
    il: str = Field(min_length=2, max_length=64)
    ilce: str = Field(min_length=2, max_length=64)
    ada: str = Field(min_length=1, max_length=32)
    parsel: str = Field(min_length=1, max_length=32)


class FieldCreateRequest(SchemaBase):
    # KR-081: wire-level request contract is explicit.
    name: str = Field(min_length=2, max_length=120)
    crop_type: CropType
    area_donum: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    parcel_ref: ParcelReference
    geometry: GeoJSONPolygon | GeoJSONMultiPolygon
    notes: str | None = Field(default=None, max_length=1000)


class FieldUpdateRequest(SchemaBase):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    crop_type: CropType | None = None
    area_donum: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    notes: str | None = Field(default=None, max_length=1000)


class GeometrySummary(SchemaBase):
    geometry_type: Literal["Polygon", "MultiPolygon"]
    coordinate_group_count: int = Field(ge=1)


class FieldResponse(SchemaBase):
    id: UUID
    owner_id: UUID
    name: str
    crop_type: CropType
    area_donum: Decimal
    parcel_ref: ParcelReference
    geometry_summary: GeometrySummary
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class PaginationMeta(SchemaBase):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class FieldListItem(SchemaBase):
    id: UUID
    name: str
    crop_type: CropType
    area_donum: Decimal
    created_at: datetime
    updated_at: datetime


class FieldListResponse(SchemaBase):
    items: list[FieldListItem] = Field(default_factory=list)
    pagination: PaginationMeta
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class FieldListFilter(SchemaBase):
    owner_id: UUID | None = None
    crop_type: CropType | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)

    @field_validator("page_size")
    @classmethod
    def normalize_page_size(cls, value: int) -> int:
        return min(value, 200)
