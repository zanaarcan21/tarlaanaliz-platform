# PATH: src/core/domain/value_objects/training_grade.py
# DESC: TrainingGrade VO; training veri kalite derecesi.
# SSOT: KR-019 (expert review), KR-081 (contract-first)
"""
TrainingGrade value object.

Uzman incelemesi (expert review) sonrası verilen training veri
kalite derecesini temsil eder. AI modeli eğitim veri setine
dahil edilecek verilerin kalitesini derecelendirir.
KR-019: Uzman incelemesi sonucu training feedback.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar


class TrainingGradeError(Exception):
    """TrainingGrade domain invariant ihlali."""


@dataclass(frozen=True)
class TrainingGrade:
    """Training veri kalite derecesi değer nesnesi (KR-019).

    Immutable (frozen=True); oluşturulduktan sonra değiştirilemez.
    Domain core'da dış dünya erişimi yoktur (IO, log yok).

    Kalite dereceleri:
    - GOLD: En yüksek kalite; doğrulanmış ve güvenilir training verisi.
    - SILVER: İyi kalite; küçük düzeltmelerle kullanılabilir.
    - BRONZE: Kabul edilebilir kalite; dikkatle kullanılmalı.
    - REJECTED: Reddedildi; training veri setine dahil edilemez.
    - PENDING: Henüz derecelendirilmemiş (varsayılan başlangıç).

    Invariants:
    - value, tanımlı geçerli derecelerden biri olmalıdır.
    """

    value: str

    # Sabit derece kodları
    GOLD: ClassVar[str] = "GOLD"
    SILVER: ClassVar[str] = "SILVER"
    BRONZE: ClassVar[str] = "BRONZE"
    REJECTED: ClassVar[str] = "REJECTED"
    PENDING: ClassVar[str] = "PENDING"

    _VALID_VALUES: ClassVar[frozenset[str]] = frozenset({
        "GOLD", "SILVER", "BRONZE", "REJECTED", "PENDING",
    })

    # Derece -> Türkçe görünen ad eşlemesi
    _DISPLAY_NAMES: ClassVar[dict[str, str]] = {
        "GOLD": "Altın",
        "SILVER": "Gümüş",
        "BRONZE": "Bronz",
        "REJECTED": "Reddedildi",
        "PENDING": "Beklemede",
    }

    # Kalite sıralaması (yüksek sayı = yüksek kalite)
    _QUALITY_ORDER: ClassVar[dict[str, int]] = {
        "REJECTED": 0,
        "PENDING": 1,
        "BRONZE": 2,
        "SILVER": 3,
        "GOLD": 4,
    }

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TrainingGradeError(
                f"value str olmalıdır, alınan tip: {type(self.value).__name__}"
            )
        normalized = self.value.strip().upper()
        if normalized != self.value:
            object.__setattr__(self, "value", normalized)
        if self.value not in self._VALID_VALUES:
            raise TrainingGradeError(
                f"Geçersiz derece: '{self.value}'. "
                f"Geçerli değerler: {sorted(self._VALID_VALUES)}"
            )

    # ------------------------------------------------------------------
    # Domain queries
    # ------------------------------------------------------------------
    @property
    def display_name(self) -> str:
        """Türkçe görünen ad."""
        return self._DISPLAY_NAMES[self.value]

    @property
    def quality_score(self) -> int:
        """Kalite sıralaması (0-4 arası)."""
        return self._QUALITY_ORDER[self.value]

    @property
    def is_usable(self) -> bool:
        """Training veri setine dahil edilebilir mi?"""
        return self.value in {self.GOLD, self.SILVER, self.BRONZE}

    @property
    def is_high_quality(self) -> bool:
        """Yüksek kaliteli mi? (GOLD veya SILVER)."""
        return self.value in {self.GOLD, self.SILVER}

    @property
    def is_rejected(self) -> bool:
        """Reddedilmiş mi?"""
        return self.value == self.REJECTED

    @property
    def is_pending(self) -> bool:
        """Henüz derecelendirilmemiş mi?"""
        return self.value == self.PENDING

    def is_better_than(self, other: TrainingGrade) -> bool:
        """Bu derece diğerinden daha iyi mi?"""
        return self.quality_score > other.quality_score

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Serileştirme için dict dönüşümü."""
        return {
            "value": self.value,
            "display_name": self.display_name,
            "is_usable": self.is_usable,
        }

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"TrainingGrade(value='{self.value}')"
