# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""API settings for middleware wiring."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_list(name: str, default: list[str]) -> list[str]:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    parsed = [item.strip() for item in raw_value.split(",") if item.strip()]
    return parsed or default


@dataclass(slots=True)
class CorsSettings:
    enabled: bool = field(default_factory=lambda: _env_bool("API_CORS_ENABLED", True))
    allow_origins: list[str] = field(default_factory=lambda: _env_list("API_CORS_ALLOW_ORIGINS", ["*"]))
    allow_methods: list[str] = field(default_factory=lambda: _env_list("API_CORS_ALLOW_METHODS", ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]))
    allow_headers: list[str] = field(default_factory=lambda: _env_list("API_CORS_ALLOW_HEADERS", ["Authorization", "Content-Type", "X-Correlation-Id"]))
    allow_credentials: bool = field(default_factory=lambda: _env_bool("API_CORS_ALLOW_CREDENTIALS", False))


@dataclass(slots=True)
class JwtSettings:
    enabled: bool = field(default_factory=lambda: _env_bool("API_JWT_ENABLED", True))
    bypass_routes: list[str] = field(default_factory=lambda: _env_list("API_JWT_BYPASS_ROUTES", ["/health", "/docs", "/openapi.json"]))
    secret: str = field(default_factory=lambda: os.getenv("API_JWT_SECRET", "dev-only-secret"))
    algorithm: str = field(default_factory=lambda: os.getenv("API_JWT_ALGORITHM", "HS256"))


@dataclass(slots=True)
class RateLimitSettings:
    enabled: bool = field(default_factory=lambda: _env_bool("API_RATE_LIMIT_ENABLED", True))
    per_minute_limit: int = field(default_factory=lambda: _env_int("API_RATE_LIMIT_PER_MINUTE", 60))
    burst: int = field(default_factory=lambda: _env_int("API_RATE_LIMIT_BURST", 20))
    bypass_routes: list[str] = field(default_factory=lambda: _env_list("API_RATE_LIMIT_BYPASS_ROUTES", ["/health", "/docs", "/openapi.json"]))


@dataclass(slots=True)
class AnomalySettings:
    enabled: bool = field(default_factory=lambda: _env_bool("API_ANOMALY_ENABLED", True))
    allowlist_routes: list[str] = field(default_factory=lambda: _env_list("API_ANOMALY_ALLOWLIST_ROUTES", ["/health", "/docs", "/openapi.json"]))
    rapid_repeat_window_seconds: int = field(default_factory=lambda: _env_int("API_ANOMALY_REPEAT_WINDOW_SECONDS", 10))
    rapid_repeat_threshold: int = field(default_factory=lambda: _env_int("API_ANOMALY_REPEAT_THRESHOLD", 8))
    large_body_threshold_bytes: int = field(default_factory=lambda: _env_int("API_ANOMALY_LARGE_BODY_BYTES", 1_000_000))


@dataclass(slots=True)
class ApiSettings:
    cors: CorsSettings = field(default_factory=CorsSettings)
    jwt: JwtSettings = field(default_factory=JwtSettings)
    rate_limit: RateLimitSettings = field(default_factory=RateLimitSettings)
    anomaly: AnomalySettings = field(default_factory=AnomalySettings)


settings = ApiSettings()
