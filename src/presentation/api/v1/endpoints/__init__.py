# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Endpoints package exports for API v1."""

from src.presentation.api.v1.endpoints.admin_audit import router as admin_audit_router
from src.presentation.api.v1.endpoints.admin_pricing import router as admin_pricing_router
from src.presentation.api.v1.endpoints.auth import router as auth_router
from src.presentation.api.v1.endpoints.expert_portal import router as expert_portal_router
from src.presentation.api.v1.endpoints.experts import router as experts_router
from src.presentation.api.v1.endpoints.fields import router as fields_router
from src.presentation.api.v1.endpoints.missions import router as missions_router
from src.presentation.api.v1.endpoints.parcels import router as parcels_router
from src.presentation.api.v1.endpoints.payment_webhooks import router as payment_webhooks_router

__all__: list[str] = [
    "admin_audit_router",
    "admin_pricing_router",
    "auth_router",
    "expert_portal_router",
    "experts_router",
    "fields_router",
    "missions_router",
    "parcels_router",
    "payment_webhooks_router",
]
