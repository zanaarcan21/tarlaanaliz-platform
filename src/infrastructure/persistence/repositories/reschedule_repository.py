"""KR-015 — Reschedule repository (scaffold)."""

from __future__ import annotations

from typing import Optional, Sequence
from sqlalchemy.orm import Session

from ..models.reschedule_request_model import RescheduleRequestModel


class RescheduleRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, row: RescheduleRequestModel) -> None:
        self.session.add(row)
        self.session.commit()

    def list_pending(self, limit: int = 100) -> Sequence[RescheduleRequestModel]:
        return (
            self.session.query(RescheduleRequestModel)
            .filter(RescheduleRequestModel.status == "REQUESTED")
            .order_by(RescheduleRequestModel.created_at.desc())
            .limit(limit)
            .all()
        )

    def get(self, req_id: str) -> Optional[RescheduleRequestModel]:
        return self.session.get(RescheduleRequestModel, req_id)
