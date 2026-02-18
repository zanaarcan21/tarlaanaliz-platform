# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-081: Contract-first test fixture factories.

from __future__ import annotations

import importlib
import uuid
from dataclasses import asdict, is_dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from src.core.domain.entities.analysis_job import AnalysisJob, AnalysisJobStatus
from src.core.domain.entities.expert import Expert, ExpertStatus
from src.core.domain.entities.field import Field, FieldStatus
from src.core.domain.entities.mission import Mission, MissionStatus
from src.core.domain.entities.payment_intent import (
    PaymentIntent,
    PaymentMethod,
    PaymentStatus,
    PaymentTargetType,
)
from src.core.domain.entities.subscription import Subscription, SubscriptionStatus
from src.core.domain.entities.user import User, UserRole

FIXED_NOW = datetime(2026, 1, 1, 9, 0, 0, tzinfo=timezone.utc)


@pytest.fixture(scope="session")
def ssot_v1_path() -> Path:
    """Locate canonical SSOT v1.0.0 document in repo."""
    candidate = Path("docs/TARLAANALIZ_SSOT_v1_0_0.txt")
    if not candidate.exists():
        pytest.skip("SSOT v1.0.0 bulunamadı: docs/TARLAANALIZ_SSOT_v1_0_0.txt")
    return candidate


@pytest.fixture(scope="session")
def fastapi_app_factory() -> Any:
    """Try to load app/create_app if API surface exists; return None otherwise."""
    try:
        module = importlib.import_module("src.presentation.api.main")
    except Exception:
        return None

    app = getattr(module, "app", None)
    create_app = getattr(module, "create_app", None)
    if app is not None:
        return lambda: app
    if callable(create_app):
        return create_app
    return None


@pytest.fixture()
def fixed_now() -> datetime:
    return FIXED_NOW


@pytest.fixture()
def user_entity(fixed_now: datetime) -> User:
    return User(
        user_id=uuid.uuid4(),
        phone_number="+905550001122",
        pin_hash="dummy-pin-hash",
        role=UserRole.FARMER_SINGLE,
        province="Konya",
        created_at=fixed_now,
        updated_at=fixed_now,
    )


@pytest.fixture()
def expert_entity(fixed_now: datetime) -> Expert:
    return Expert(
        expert_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        province="Konya",
        max_daily_quota=25,
        created_by_admin_user_id=uuid.uuid4(),
        specialization=["NDVI"],
        status=ExpertStatus.ACTIVE,
        created_at=fixed_now,
        updated_at=fixed_now,
    )


@pytest.fixture()
def field_entity(user_entity: User, fixed_now: datetime) -> Field:
    return Field(
        field_id=uuid.uuid4(),
        user_id=user_entity.user_id,
        province="Konya",
        district="Selcuklu",
        village="Sancak",
        ada="123",
        parsel="45",
        area_m2=Decimal("2500000"),
        status=FieldStatus.ACTIVE,
        crop_type="WHEAT",
        created_at=fixed_now,
        updated_at=fixed_now,
        geometry={
            "type": "Polygon",
            "coordinates": [[[32.0, 37.0], [32.1, 37.0], [32.1, 37.1], [32.0, 37.1], [32.0, 37.0]]],
        },
    )


@pytest.fixture()
def mission_entity(field_entity: Field, fixed_now: datetime) -> Mission:
    return Mission(
        mission_id=uuid.uuid4(),
        field_id=field_entity.field_id,
        requested_by_user_id=field_entity.user_id,
        crop_type="WHEAT",
        analysis_type="MULTISPECTRAL",
        status=MissionStatus.PLANNED,
        price_snapshot_id=uuid.uuid4(),
        created_at=fixed_now,
    )


@pytest.fixture()
def subscription_entity(user_entity: User, field_entity: Field, fixed_now: datetime) -> Subscription:
    return Subscription(
        subscription_id=uuid.uuid4(),
        farmer_user_id=user_entity.user_id,
        field_id=field_entity.field_id,
        crop_type="WHEAT",
        analysis_type="MULTISPECTRAL",
        interval_days=14,
        start_date=fixed_now.date(),
        end_date=(fixed_now + timedelta(days=180)).date(),
        next_due_at=fixed_now + timedelta(days=14),
        status=SubscriptionStatus.PENDING_PAYMENT,
        price_snapshot_id=uuid.uuid4(),
        created_at=fixed_now,
        updated_at=fixed_now,
    )


@pytest.fixture()
def payment_intent_entity(user_entity: User, mission_entity: Mission, fixed_now: datetime) -> PaymentIntent:
    return PaymentIntent(
        payment_intent_id=uuid.uuid4(),
        payer_user_id=user_entity.user_id,
        target_type=PaymentTargetType.MISSION,
        target_id=mission_entity.mission_id,
        amount_kurus=150_000,
        currency="TRY",
        method=PaymentMethod.IBAN_TRANSFER,
        status=PaymentStatus.PAYMENT_PENDING,
        payment_ref="PAY-20260101-DUMMY",
        price_snapshot_id=uuid.uuid4(),
        created_at=fixed_now,
        updated_at=fixed_now,
    )


@pytest.fixture()
def analysis_job_entity(field_entity: Field, mission_entity: Mission, fixed_now: datetime) -> AnalysisJob:
    return AnalysisJob(
        analysis_job_id=uuid.uuid4(),
        mission_id=mission_entity.mission_id,
        field_id=field_entity.field_id,
        crop_type="WHEAT",
        analysis_type="MULTISPECTRAL",
        model_id="model-v1",
        model_version="1.0.0",
        status=AnalysisJobStatus.PENDING,
        created_at=fixed_now,
        updated_at=fixed_now,
    )


def as_contract_payload(entity: Any) -> dict[str, Any]:
    """KR-081 helper: entity -> dict for explicit field assertions."""
    if is_dataclass(entity):
        payload = asdict(entity)
    elif isinstance(entity, dict):
        payload = dict(entity)
    else:
        raise TypeError(f"Unsupported fixture type for contract payload: {type(entity)!r}")
    return payload


__all__ = ["FIXED_NOW", "as_contract_payload"]
