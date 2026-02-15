# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

from __future__ import annotations

import datetime as dt
import uuid

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.sqlalchemy.base import Base


class AnalysisJobModel(Base):
    """AnalysisJob persistence model."""

    __tablename__ = "analysis_jobs"

    # KR-081: AnalysisJob contract-first JSON payload pointer/version alanları.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    schema_version: Mapped[str] = mapped_column(String(32), nullable=False)
    input_payload_uri: Mapped[str] = mapped_column(Text, nullable=False)
    output_payload_uri: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")

    # KR-018: Kalibrasyon hard-gate sağlanmadan analiz tamamlanamaz.
    calibration_gate_passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
