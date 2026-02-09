# PATH: src/core/domain/events/analysis_events.py
# DESC: Analysis domain event'leri (KR-017, KR-018).

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from src.core.domain.events.base import DomainEvent


@dataclass(frozen=True)
class AnalysisRequested(DomainEvent):
    """Analiz talebi oluşturuldu (KR-017).

    Mission veya subscription akışından tetiklenir.
    requires_calibrated=True zorunluluğu KR-018 ile sağlanır.
    """

    mission_id: uuid.UUID = field(default_factory=uuid.uuid4)
    field_id: uuid.UUID = field(default_factory=uuid.uuid4)
    crop_type: str = ""
    requires_calibrated: bool = True  # KR-018: hard gate

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "mission_id": str(self.mission_id),
            "field_id": str(self.field_id),
            "crop_type": self.crop_type,
            "requires_calibrated": self.requires_calibrated,
        })
        return base


@dataclass(frozen=True)
class AnalysisStarted(DomainEvent):
    """Analiz işleme başladı (worker tarafından)."""

    analysis_job_id: uuid.UUID = field(default_factory=uuid.uuid4)
    mission_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "analysis_job_id": str(self.analysis_job_id),
            "mission_id": str(self.mission_id),
        })
        return base


@dataclass(frozen=True)
class AnalysisCompleted(DomainEvent):
    """Analiz tamamlandı; sonuçlar hazır (KR-017)."""

    analysis_job_id: uuid.UUID = field(default_factory=uuid.uuid4)
    mission_id: uuid.UUID = field(default_factory=uuid.uuid4)
    field_id: uuid.UUID = field(default_factory=uuid.uuid4)
    confidence_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "analysis_job_id": str(self.analysis_job_id),
            "mission_id": str(self.mission_id),
            "field_id": str(self.field_id),
            "confidence_score": self.confidence_score,
        })
        return base


@dataclass(frozen=True)
class AnalysisFailed(DomainEvent):
    """Analiz işlemi başarısız oldu."""

    analysis_job_id: uuid.UUID = field(default_factory=uuid.uuid4)
    mission_id: uuid.UUID = field(default_factory=uuid.uuid4)
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "analysis_job_id": str(self.analysis_job_id),
            "mission_id": str(self.mission_id),
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class CalibrationValidated(DomainEvent):
    """Radyometrik kalibrasyon doğrulandı (KR-018).

    Worker QC gate sonucu: PASS/WARN/FAIL.
    FAIL durumunda AnalysisJob başlatılamaz (hard gate).
    """

    mission_id: uuid.UUID = field(default_factory=uuid.uuid4)
    batch_id: uuid.UUID = field(default_factory=uuid.uuid4)
    qc_result: str = ""  # PASS | WARN | FAIL

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "mission_id": str(self.mission_id),
            "batch_id": str(self.batch_id),
            "qc_result": self.qc_result,
        })
        return base


@dataclass(frozen=True)
class LowConfidenceDetected(DomainEvent):
    """Düşük güven skoru tespit edildi; expert review tetiklenir (KR-019)."""

    analysis_job_id: uuid.UUID = field(default_factory=uuid.uuid4)
    field_id: uuid.UUID = field(default_factory=uuid.uuid4)
    confidence_score: float = 0.0
    threshold: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "analysis_job_id": str(self.analysis_job_id),
            "field_id": str(self.field_id),
            "confidence_score": self.confidence_score,
            "threshold": self.threshold,
        })
        return base
