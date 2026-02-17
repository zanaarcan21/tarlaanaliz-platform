# PATH: src/infrastructure/integrations/storage/__init__.py
# DESC: Storage integrations package.
"""Storage provider integration adapters."""

from src.infrastructure.integrations.storage.s3_storage import S3StorageIntegration

__all__: list[str] = [
    "S3StorageIntegration",
]
