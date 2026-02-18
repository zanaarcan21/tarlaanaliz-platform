# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/parcel_schemas.py
# DESC: Parsel lookup request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


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


class ParcelLookupRequest(SchemaBase):
    # KR-081: lookup request contract kept explicit and deterministic.
    il: str = Field(min_length=2, max_length=64)
    ilce: str = Field(min_length=2, max_length=64)
    ada: str = Field(min_length=1, max_length=32)
    parsel: str = Field(min_length=1, max_length=32)
    year: int | None = Field(default=None, ge=1900, le=2200)

    @field_validator("ada", "parsel", mode="before")
    @classmethod
    def normalize_numeric_ref(cls, value: str | int) -> str:
        return str(value).strip()


class ParcelLookupResponse(SchemaBase):
    parcel_ref: ParcelReference
    geometry: GeoJSONPolygon | GeoJSONMultiPolygon
    area_donum: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    source: str = Field(min_length=2, max_length=64)
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
