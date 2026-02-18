# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
# KR-015: Weather block and force-majeure scheduling behavior.
# KR-081: Payload/contract checks.

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from src.core.domain.entities.weather_block_report import WeatherBlockReport
from src.core.domain.services.weather_validator import (
    FlightRecommendation,
    WeatherData,
    WeatherSeverity,
    WeatherValidator,
)


def test_weather_block_report_requires_reason() -> None:
    with pytest.raises(ValueError, match="reason is required"):
        WeatherBlockReport(
            weather_block_id=uuid.uuid4(),
            mission_id=uuid.uuid4(),
            field_id=uuid.uuid4(),
            reported_at=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
            reason="",
            created_at=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
        )


def test_kr015_force_majeure_report_from_fake_weather_data() -> None:
    validator = WeatherValidator()

    result = validator.validate(
        mission_id=uuid.uuid4(),
        weather_data=WeatherData(
            condition="storm",
            wind_speed_kmh=45.0,
            visibility_km=1.0,
            precipitation_mm=8.0,
        ),
    )

    assert result.severity in {WeatherSeverity.HIGH, WeatherSeverity.EXTREME}
    assert result.recommendation in {FlightRecommendation.NO_FLY, FlightRecommendation.GROUND_ALL}
    assert validator.is_force_majeure(result) is True


def test_weather_block_contract_fields_present() -> None:
    report = WeatherBlockReport(
        weather_block_id=uuid.uuid4(),
        mission_id=uuid.uuid4(),
        field_id=uuid.uuid4(),
        reported_at=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
        reason="strong_wind",
        created_at=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
    )

    payload = report.__dict__
    for key in ("weather_block_id", "mission_id", "field_id", "reason", "created_at"):
        assert key in payload, f"KR-081 contract field missing for weather block report: {key}"


def test_weather_block_api_unavailable_yet(fastapi_app_factory: object) -> None:
    if fastapi_app_factory is None:
        pytest.skip("FastAPI app factory bulunamadı; weather block endpoint integration testi skip edildi.")

    pytest.xfail("weather-block endpointleri henüz implement değil; domain doğrulaması aktif.")
