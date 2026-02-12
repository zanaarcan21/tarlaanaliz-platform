# PATH: src/infrastructure/messaging/websocket/__init__.py
# DESC: WebSocket messaging package.
"""WebSocket messaging adapters."""

from src.infrastructure.messaging.websocket.notification_manager import (
    Notification,
    WebSocketNotificationManager,
)

__all__: list[str] = [
    "Notification",
    "WebSocketNotificationManager",
]
