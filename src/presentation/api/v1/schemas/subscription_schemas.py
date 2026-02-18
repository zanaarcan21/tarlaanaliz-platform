# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# PATH: src/presentation/api/v1/schemas/subscription_schemas.py
# DESC: Subscription request/response schema.
# TODO: Implement this file.

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class CurrencyCode(str, Enum):
    try_ = "TRY"
    usd = "USD"
    eur = "EUR"


class SubscriptionStatus(str, Enum):
    pending = "pending"
    active = "active"
    expired = "expired"
    cancelled = "cancelled"


class SubscriptionLimits(SchemaBase):
    max_donum: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    max_jobs: int = Field(ge=1, le=10000)


class SubscriptionCreateRequest(SchemaBase):
    # KR-081: subscription wire contract is fixed for presentation API.
    plan_id: UUID | None = None
    season_package_id: UUID | None = None
    field_id: UUID | None = None
    starts_at: datetime
    ends_at: datetime
    price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    currency: CurrencyCode | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> SubscriptionCreateRequest:
        if not self.plan_id and not self.season_package_id:
            raise ValueError("Either plan_id or season_package_id must be provided")
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be greater than starts_at")
        if (self.price is None) ^ (self.currency is None):
            raise ValueError("price and currency must be provided together")
        return self


class SubscriptionResponse(SchemaBase):
    id: UUID
    owner_id: UUID
    plan_id: UUID | None = None
    season_package_id: UUID | None = None
    field_id: UUID | None = None
    starts_at: datetime
    ends_at: datetime
    status: SubscriptionStatus
    limits: SubscriptionLimits
    price: Decimal | None = None
    currency: CurrencyCode | None = None
    created_at: datetime
    updated_at: datetime
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)


class PaginationMeta(SchemaBase):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class SubscriptionListResponse(SchemaBase):
    items: list[SubscriptionResponse] = Field(default_factory=list)
    pagination: PaginationMeta
    corr_id: str | None = Field(default=None, min_length=8, max_length=128)
