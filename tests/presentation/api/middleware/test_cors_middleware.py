# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.api.middleware.cors_middleware import add_cors_middleware
from src.presentation.api.settings import settings


def _app() -> FastAPI:
    app = FastAPI()
    add_cors_middleware(app)

    @app.get("/sample")
    def sample() -> dict[str, str]:
        return {"ok": "ok"}

    return app


def test_cors_preflight_options_success(monkeypatch) -> None:
    monkeypatch.setattr(settings.cors, "allow_origins", ["https://example.com"])
    monkeypatch.setattr(settings.cors, "allow_methods", ["GET", "OPTIONS"])
    monkeypatch.setattr(settings.cors, "allow_headers", ["Authorization", "Content-Type"])

    client = TestClient(_app())
    response = client.options(
        "/sample",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://example.com"


def test_cors_disallowed_origin(monkeypatch) -> None:
    monkeypatch.setattr(settings.cors, "allow_origins", ["https://example.com"])
    client = TestClient(_app())

    response = client.options(
        "/sample",
        headers={
            "Origin": "https://blocked.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 400


def test_cors_disabled(monkeypatch) -> None:
    monkeypatch.setattr(settings.cors, "enabled", False)
    try:
        client = TestClient(_app())
        response = client.get("/sample", headers={"Origin": "https://example.com"})
        assert response.status_code == 200
        assert "access-control-allow-origin" not in response.headers
    finally:
        monkeypatch.setattr(settings.cors, "enabled", True)


def test_cors_simple_request_sets_headers(monkeypatch) -> None:
    monkeypatch.setattr(settings.cors, "allow_origins", ["https://example.com"])
    client = TestClient(_app())

    response = client.get("/sample", headers={"Origin": "https://example.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://example.com"
