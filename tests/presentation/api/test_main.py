# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

from __future__ import annotations

from fastapi.testclient import TestClient

from src.presentation.api.main import create_app


def test_create_app_importable() -> None:
    app = create_app()
    assert app is not None


def test_health_returns_200() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200


def test_health_has_correlation_id_header() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert "X-Correlation-Id" in response.headers
