"""KR-015 — reschedule_request SQLAlchemy model (scaffold)."""

from __future__ import annotations

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RescheduleRequestModel(Base):  # type: ignore[misc, valid-type]
    __tablename__ = "subscription_reschedule_requests"

    id = Column(String(36), primary_key=True)
    subscription_id = Column(String(36), nullable=False, index=True)
    mission_id = Column(String(36), nullable=True, index=True)
    occurrence_ref = Column(String(64), nullable=True)

    requested_date = Column(DateTime(timezone=True), nullable=False)

    status = Column(String(32), nullable=False)  # REQUESTED|APPROVED|REJECTED|CANCELED
    requested_by = Column(String(36), nullable=False)
    reviewed_by = Column(String(36), nullable=True)

    reason = Column(Text(), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
