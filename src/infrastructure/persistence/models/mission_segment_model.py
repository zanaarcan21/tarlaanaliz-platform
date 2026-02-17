"""KR-015 (optional) — mission_segment model scaffold."""

from __future__ import annotations

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MissionSegmentModel(Base):  # type: ignore[misc, valid-type]
    __tablename__ = "mission_segments"

    id = Column(String(36), primary_key=True)
    mission_id = Column(String(36), nullable=False, index=True)
    segment_no = Column(Integer, nullable=False)
    area_donum = Column(Integer, nullable=False)
    assigned_pilot_id = Column(String(36), nullable=True)

    status = Column(String(32), nullable=False, default="PLANNED")
    created_at = Column(DateTime(timezone=True), nullable=False)
