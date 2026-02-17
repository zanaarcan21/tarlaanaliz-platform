"""KR-015 (optional) — mission_segment repository scaffold."""

from __future__ import annotations

from typing import Sequence
from sqlalchemy.orm import Session

from ..models.mission_segment_model import MissionSegmentModel


class MissionSegmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_many(self, segments: Sequence[MissionSegmentModel]) -> None:
        self.session.add_all(list(segments))
        self.session.commit()
