# PATH: src/infrastructure/messaging/__init__.py
# DESC: Infrastructure messaging package: event bus ve kuyruk adapter'ları.
"""
Infrastructure messaging adapters.

Amaç: Python paket başlangıcı; modül dışa aktarım (exports) ve namespace düzeni.
Sorumluluk: Python paket başlangıcı; import yüzeyini (public API) düzenler.
Notlar/SSOT: KR-015, KR-018, KR-033, KR-081 ile tutarlı kalır.
"""

from src.infrastructure.messaging.event_publisher import EventPublisher
from src.infrastructure.messaging.rabbitmq.ai_feedback_publisher import (
    AIFeedbackPublisher,
)
from src.infrastructure.messaging.rabbitmq.consumer import RabbitMQConsumer
from src.infrastructure.messaging.rabbitmq.publisher import RabbitMQPublisher
from src.infrastructure.messaging.rabbitmq.training_feedback_publisher import (
    TrainingFeedbackPublisher,
)
from src.infrastructure.messaging.rabbitmq_event_bus_impl import RabbitMQEventBus
from src.infrastructure.messaging.websocket.notification_manager import (
    Notification,
    WebSocketNotificationManager,
)

__all__: list[str] = [
    # RabbitMQ adapters
    "AIFeedbackPublisher",
    "RabbitMQConsumer",
    "RabbitMQPublisher",
    "TrainingFeedbackPublisher",
    # Event bus
    "EventPublisher",
    "RabbitMQEventBus",
    # WebSocket
    "Notification",
    "WebSocketNotificationManager",
]
