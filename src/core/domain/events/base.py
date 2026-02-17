# PATH: src/core/domain/events/base.py
# DESC: Domain event base class'ı; tüm event'ler için ortak yapı.

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class DomainEvent:
    """Tüm domain event'leri için ortak taban sınıf.

    Immutable (frozen=True); oluşturulduktan sonra değiştirilemez.
    Application layer tarafından publish/handle edilir.
    Domain core'da dış dünya erişimi yoktur (IO, log yok).
    """

    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def event_type(self) -> str:
        """Event sınıf adını döner (routing/dispatch için)."""
        return self.__class__.__name__

    def to_dict(self) -> dict[str, Any]:
        """Serileştirme için dict dönüşümü.

        Alt sınıflar ek alanlarını eklemek için override edebilir.
        """
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
        }
