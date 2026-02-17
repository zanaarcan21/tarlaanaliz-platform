# PATH: src/infrastructure/config/__init__.py
"""Infrastructure configuration package."""

from src.infrastructure.config.settings import Settings, get_settings

__all__: list[str] = [
    "Settings",
    "get_settings",
]
