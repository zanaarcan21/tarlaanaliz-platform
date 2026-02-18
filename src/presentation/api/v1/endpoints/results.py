# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""Analysis results endpoints (layer list + summary)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/results", tags=["results"])


class ResultLayerDTO(BaseModel):
    layer_name: str
    uri: str


class ResultSummaryDTO(BaseModel):
    analysis_job_id: str
    mission_id: str
    layers: list[ResultLayerDTO]
    quality_status: str = Field(default="ready")


class ResultsService(Protocol):
    def get_summary(self, analysis_job_id: str, actor_subject: str) -> ResultSummaryDTO:
        ...


@dataclass(slots=True)
class _InMemoryResultsService:
    def get_summary(self, analysis_job_id: str, actor_subject: str) -> ResultSummaryDTO:
        _ = actor_subject
        return ResultSummaryDTO(
            analysis_job_id=analysis_job_id,
            mission_id="msn-1",
            layers=[ResultLayerDTO(layer_name="ndvi", uri="s3://demo/ndvi.tif")],
        )


def get_results_service() -> ResultsService:
    return _InMemoryResultsService()


def _require_subject(request: Request) -> str:
    user = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return str(getattr(user, "subject", ""))


@router.get("/{analysis_job_id}/summary", response_model=ResultSummaryDTO)
def get_result_summary(
    request: Request,
    analysis_job_id: str,
    service: ResultsService = Depends(get_results_service),
) -> ResultSummaryDTO:
    # KR-018: calibration hard-gate is enforced by application/domain prior to result publication.
    subject = _require_subject(request)
    return service.get_summary(analysis_job_id=analysis_job_id, actor_subject=subject)
