"""KR-015 — Pilot notification service (SMS + in-app + websocket).

Bu servis, atama/reschedule/reassignment bildirimlerini tek merkezde toplar.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol


class SmsGateway(Protocol):
    def send(self, to_phone: str, message: str) -> None: ...


class WebsocketNotifier(Protocol):
    def notify(self, user_id: str, event: str, payload: dict[str, Any]) -> None: ...


@dataclass
class PilotNotificationService:
    sms_gateway: Optional[SmsGateway] = None
    websocket_notifier: Optional[WebsocketNotifier] = None

    def notify_assignment(self, pilot_user_id: str, phone: str, mission_id: str) -> None:
        msg = f"Yeni görev atandı: {mission_id}"
        if self.sms_gateway:
            self.sms_gateway.send(phone, msg)
        if self.websocket_notifier:
            self.websocket_notifier.notify(pilot_user_id, "MISSION_ASSIGNED", {"mission_id": mission_id})
