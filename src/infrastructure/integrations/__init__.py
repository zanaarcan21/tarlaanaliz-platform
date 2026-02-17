# PATH: src/infrastructure/integrations/__init__.py
# DESC: Infrastructure integrations package: provider-spesifik adapter'lar.
"""Infrastructure integrations: provider-specific adapter implementations.

Port interface'leri core'da tanımlıdır; burada yalnızca provider-spesifik
implementasyonlar bulunur.
"""

from src.infrastructure.integrations.cloudflare import CloudflareDDoSAdapter
from src.infrastructure.integrations.payments import ProviderPaymentGateway
from src.infrastructure.integrations.sms import NetGSMAdapter, TwilioSMSAdapter
from src.infrastructure.integrations.storage import S3StorageIntegration

__all__: list[str] = [
    "CloudflareDDoSAdapter",
    "ProviderPaymentGateway",
    "NetGSMAdapter",
    "TwilioSMSAdapter",
    "S3StorageIntegration",
]
