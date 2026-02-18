# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Phone + PIN authentication endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/auth", tags=["auth"])


class PhonePinLoginRequest(BaseModel):
    phone: str = Field(min_length=10, max_length=20)
    pin: str = Field(min_length=4, max_length=12)


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    subject: str
    phone_verified: bool = True


class AuthRefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=8)


class PhonePinAuthService(Protocol):
    def login(self, phone: str, pin: str) -> AuthTokenResponse:
        ...

    def refresh(self, refresh_token: str) -> AuthTokenResponse:
        ...


@dataclass(slots=True)
class _InMemoryPhonePinAuthService:
    def login(self, phone: str, pin: str) -> AuthTokenResponse:
        # KR-081: explicit auth contract; no email/TCKN/OTP fields accepted.
        if phone != "+905555555555" or pin != "1234":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return AuthTokenResponse(access_token="demo-access-token", subject="user-1")

    def refresh(self, refresh_token: str) -> AuthTokenResponse:
        if refresh_token != "demo-refresh-token":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return AuthTokenResponse(access_token="demo-access-token-refreshed", subject="user-1")


def get_phone_pin_auth_service() -> PhonePinAuthService:
    return _InMemoryPhonePinAuthService()


@router.post("/phone-pin/login", response_model=AuthTokenResponse)
def phone_pin_login(payload: PhonePinLoginRequest, service: PhonePinAuthService = Depends(get_phone_pin_auth_service)) -> AuthTokenResponse:
    return service.login(phone=payload.phone, pin=payload.pin)


@router.post("/phone-pin/refresh", response_model=AuthTokenResponse)
def phone_pin_refresh(payload: AuthRefreshRequest, service: PhonePinAuthService = Depends(get_phone_pin_auth_service)) -> AuthTokenResponse:
    return service.refresh(refresh_token=payload.refresh_token)


@router.get("/me")
def me(request: Request) -> dict[str, str | bool]:
    user = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return {
        "subject": str(getattr(user, "subject", "")),
        "phone_verified": bool(getattr(user, "phone_verified", False)),
    }
