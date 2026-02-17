# PATH: src/infrastructure/integrations/payments/__init__.py
# DESC: Payment integrations package.
"""Payment provider integration adapters."""

from src.infrastructure.integrations.payments.provider_gateway import (
    ProviderPaymentGateway,
)

__all__: list[str] = [
    "ProviderPaymentGateway",
]
