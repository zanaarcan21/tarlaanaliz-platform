# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.api.middleware.rate_limit_middleware import RateLimitMiddleware
from src.presentation.api.settings import settings


def _app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/limited")
    def limited() -> dict[str, str]:
        return {"ok": "ok"}

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"ok": "ok"}

    return app


def test_rate_limit_allows_initial_requests(monkeypatch) -> None:
    monkeypatch.setattr(settings.rate_limit, "per_minute_limit", 2)
    monkeypatch.setattr(settings.rate_limit, "burst", 0)
    client = TestClient(_app())

    first = client.get("/limited")
    second = client.get("/limited")

    assert first.status_code == 200
    assert second.status_code == 200


def test_rate_limit_blocks_when_exceeded(monkeypatch) -> None:
    monkeypatch.setattr(settings.rate_limit, "per_minute_limit", 1)
    monkeypatch.setattr(settings.rate_limit, "burst", 0)
    client = TestClient(_app())

    _ = client.get("/limited")
    blocked = client.get("/limited")

    assert blocked.status_code == 429
    assert "Retry-After" in blocked.headers
    assert "X-Correlation-Id" in blocked.headers


def test_rate_limit_bypass_route(monkeypatch) -> None:
    monkeypatch.setattr(settings.rate_limit, "per_minute_limit", 0)
    monkeypatch.setattr(settings.rate_limit, "burst", 0)
    client = TestClient(_app())

    response = client.get("/health")
    assert response.status_code == 200


def test_rate_limit_disabled(monkeypatch) -> None:
    monkeypatch.setattr(settings.rate_limit, "enabled", False)
    try:
        client = TestClient(_app())
        response = client.get("/limited")
        assert response.status_code == 200
    finally:
        monkeypatch.setattr(settings.rate_limit, "enabled", True)
