# PATH: src/core/domain/entities/weather_block_report.py
# DESC: WeatherBlockReport; hava nedeniyle uçuş iptal kanıt/akış modeli.

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


class WeatherBlockReportError(Exception):
    """WeatherBlockReport domain invariant ihlali."""


@dataclass
class WeatherBlockReport:
    """Hava koşulları nedeniyle uçuş iptal raporu (KR-015-3, KR-015-5).

    Yaşam döngüsü: REPORTED -> VERIFIED | REJECTED ; VERIFIED -> RESOLVED
    - VERIFIED olunca Mission REPLAN_QUEUE'ya alınır (neden: WEATHER_BLOCK).
    - Weather block (force majeure) yeniden planlaması reschedule token tüketmez.
    - Doğrulama: sistem hava verisi doğrulama + yerel istasyon operatörü onayı.

    Domain invariants:
    - mission_id zorunludur.
    - weather_condition boş olamaz.
    - Status geçişleri: REPORTED -> VERIFIED | REJECTED (geri alınamaz).
    - Doğrulama alanları (verified_by_admin_id, verified_at) sadece VERIFIED/REJECTED'de set edilir.
    - reschedule_token_consumed her zaman False kalır (force majeure).
    """

    weather_block_report_id: uuid.UUID
    mission_id: uuid.UUID
    pilot_id: uuid.UUID | None
    reported_at: datetime
    status: str  # REPORTED | VERIFIED | REJECTED | RESOLVED
    weather_condition: str  # rain, wind, cloud, fog vb.
    notes: str | None = None
    evidence_blob_ids: list[str] = field(default_factory=list)
    verified_by_admin_id: uuid.UUID | None = None
    verified_at: datetime | None = None
    auto_rescheduled_mission_id: uuid.UUID | None = None
    reschedule_token_consumed: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Domain event biriktirme (application layer tarafından tüketilir)
    _domain_events: list[Any] = field(default_factory=list, repr=False, compare=False)

    _VALID_STATUSES: frozenset[str] = field(
        default=frozenset({"REPORTED", "VERIFIED", "REJECTED", "RESOLVED"}),
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.mission_id:
            raise WeatherBlockReportError("mission_id zorunludur.")
        if self.status not in self._VALID_STATUSES:
            raise WeatherBlockReportError(
                f"Geçersiz status: {self.status}. Geçerli: {self._VALID_STATUSES}"
            )
        if not self.weather_condition or not self.weather_condition.strip():
            raise WeatherBlockReportError("weather_condition boş olamaz.")

    @classmethod
    def create(
        cls,
        mission_id: uuid.UUID,
        pilot_id: uuid.UUID | None,
        weather_condition: str,
        notes: str | None = None,
        evidence_blob_ids: list[str] | None = None,
    ) -> WeatherBlockReport:
        """Yeni weather block raporu oluşturur (status: REPORTED)."""
        return cls(
            weather_block_report_id=uuid.uuid4(),
            mission_id=mission_id,
            pilot_id=pilot_id,
            reported_at=datetime.now(timezone.utc),
            status="REPORTED",
            weather_condition=weather_condition.strip().lower(),
            notes=notes,
            evidence_blob_ids=evidence_blob_ids or [],
        )

    def verify(
        self,
        admin_id: uuid.UUID,
        rescheduled_mission_id: uuid.UUID | None = None,
    ) -> None:
        """Raporu doğrular (REPORTED -> VERIFIED).

        KR-015-5: Weather block (force majeure) reschedule token tüketmez.
        """
        if self.status != "REPORTED":
            raise WeatherBlockReportError(
                f"Sadece REPORTED durumundaki rapor doğrulanabilir. Mevcut: {self.status}"
            )
        self.status = "VERIFIED"
        self.verified_by_admin_id = admin_id
        self.verified_at = datetime.now(timezone.utc)
        self.auto_rescheduled_mission_id = rescheduled_mission_id
        # KR-015-5: force majeure → token tüketilmez
        self.reschedule_token_consumed = False

    def reject(self, admin_id: uuid.UUID) -> None:
        """Raporu reddeder (REPORTED -> REJECTED)."""
        if self.status != "REPORTED":
            raise WeatherBlockReportError(
                f"Sadece REPORTED durumundaki rapor reddedilebilir. Mevcut: {self.status}"
            )
        self.status = "REJECTED"
        self.verified_by_admin_id = admin_id
        self.verified_at = datetime.now(timezone.utc)

    def resolve(self) -> None:
        """Raporu çözümlendi olarak işaretler (VERIFIED -> RESOLVED)."""
        if self.status != "VERIFIED":
            raise WeatherBlockReportError(
                f"Sadece VERIFIED durumundaki rapor çözümlenebilir. Mevcut: {self.status}"
            )
        self.status = "RESOLVED"

    @property
    def is_pending(self) -> bool:
        return self.status == "REPORTED"

    @property
    def is_verified(self) -> bool:
        return self.status == "VERIFIED"

    @property
    def is_rejected(self) -> bool:
        return self.status == "REJECTED"

    @property
    def is_resolved(self) -> bool:
        return self.status == "RESOLVED"

    def collect_events(self) -> list[Any]:
        """Biriken domain event'lerini toplar ve temizler."""
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
