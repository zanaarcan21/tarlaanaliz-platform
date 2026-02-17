# PATH: src/core/ports/messaging/__init__.py
# DESC: Messaging ports module: event publish/subscribe.
"""Messaging ports public API."""

from src.core.ports.messaging.event_bus import EventBus, EventHandler

__all__: list[str] = [
    "EventBus",
    "EventHandler",
]
