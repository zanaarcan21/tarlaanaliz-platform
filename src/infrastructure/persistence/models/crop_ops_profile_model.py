# PATH: src/infrastructure/persistence/models/crop_ops_profile_model.py
# DESC: CropOpsProfile DB modeli.
"""CropOpsProfile DB modeli (KR-015-1).

crop_ops_profiles tablosu: Bitki bazli operasyonel kapasite profili.
Admin tarafindan her CropType icin tanimlanan gunluk kapasite, sistem kota ve
tarama araligi parametrelerini saklar.

Tablo semasi: alembic/versions/20260102_005_pilots.py (revision 005).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, cast

from sqlalchemy import Column, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import DeclarativeBase

from src.core.domain.value_objects.crop_ops_profile import CropOpsProfile
from src.core.domain.value_objects.crop_type import CropType


class _Base(DeclarativeBase):
    """Gecici declarative base.

    Ortak Base (src.infrastructure.persistence.sqlalchemy.models.base)
    implemente edildiginde bu sinif kaldirilip oradan import edilecektir.
    """


# PostgreSQL 'crop_type' enum'u migration 002'de olusturulmustur; create_type=False.
_crop_type_enum = ENUM(
    "PAMUK",
    "ANTEP_FISTIGI",
    "MISIR",
    "BUGDAY",
    "AYCICEGI",
    "UZUM",
    "ZEYTIN",
    "KIRMIZI_MERCIMEK",
    name="crop_type",
    create_type=False,
)


class CropOpsProfileModel(_Base):
    """crop_ops_profiles tablosu icin SQLAlchemy modeli (KR-015-1).

    Her bitki tipi icin tek bir profil satiri bulunur (crop_type UNIQUE).
    """

    __tablename__ = "crop_ops_profiles"

    profile_id: Any = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    crop_type: Any = Column(
        _crop_type_enum,
        nullable=False,
        unique=True,
    )
    daily_capacity_donum: Any = Column(
        Integer,
        nullable=False,
        server_default=text("2750"),
    )
    system_seed_quota: Any = Column(
        Integer,
        nullable=False,
        server_default=text("1500"),
    )
    recommended_interval_days: Any = Column(
        Integer,
        nullable=True,
    )
    created_at: Any = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at: Any = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    def to_domain(self) -> CropOpsProfile:
        """DB satirini domain CropOpsProfile VO'suna donusturur.

        Not: overage_tolerance DB'de saklanmaz; varsayilan deger kullanilir.
        """
        return CropOpsProfile(
            crop_type=CropType(code=cast(str, self.crop_type)),
            daily_capacity_donum=cast(int, self.daily_capacity_donum),
            system_seed_quota=cast(int, self.system_seed_quota),
            overage_tolerance=CropOpsProfile.DEFAULT_OVERAGE_TOLERANCE,
        )

    @classmethod
    def from_domain(
        cls,
        vo: CropOpsProfile,
        *,
        profile_id: uuid.UUID | None = None,
    ) -> CropOpsProfileModel:
        """Domain CropOpsProfile VO'sundan DB modeli olusturur.

        recommended_interval_days, CropType'in tavsiye tarama araliginin
        alt siniri olarak atanir.
        """
        min_interval, _ = vo.crop_type.recommended_scan_interval
        return cls(
            profile_id=profile_id or uuid.uuid4(),
            crop_type=vo.crop_type.code,
            daily_capacity_donum=vo.daily_capacity_donum,
            system_seed_quota=vo.system_seed_quota,
            recommended_interval_days=min_interval,
        )

    def update_from_domain(self, vo: CropOpsProfile) -> None:
        """Mevcut DB satirini domain VO ile gunceller.

        profile_id ve created_at degismez; updated_at DB trigger/uygulama
        katmaninda guncellenir.
        """
        self.crop_type = vo.crop_type.code
        self.daily_capacity_donum = vo.daily_capacity_donum
        self.system_seed_quota = vo.system_seed_quota
        min_interval, _ = vo.crop_type.recommended_scan_interval
        self.recommended_interval_days = min_interval

    def to_dict(self) -> dict[str, Any]:
        """Seri hale getirme (API response, logging)."""
        return {
            "profile_id": str(self.profile_id),
            "crop_type": self.crop_type,
            "daily_capacity_donum": self.daily_capacity_donum,
            "system_seed_quota": self.system_seed_quota,
            "recommended_interval_days": self.recommended_interval_days,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return (
            f"CropOpsProfileModel("
            f"profile_id={self.profile_id!r}, "
            f"crop_type={self.crop_type!r}, "
            f"capacity={self.daily_capacity_donum})"
        )
