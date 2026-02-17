# PATH: src/infrastructure/integrations/cloudflare/__init__.py
# DESC: Cloudflare integrations package.
"""Cloudflare integration adapters."""

from src.infrastructure.integrations.cloudflare.ddos_protection import (
    CloudflareDDoSAdapter,
)

__all__: list[str] = [
    "CloudflareDDoSAdapter",
]
