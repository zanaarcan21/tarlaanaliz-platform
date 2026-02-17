"""KR-015 — Assignment policy (source + reason) standardization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AssignmentSource(str, Enum):
    SYSTEM_SEED = "SYSTEM_SEED"
    PULL = "PULL"


class AssignmentReason(str, Enum):
    AUTO_DISPATCH = "AUTO_DISPATCH"
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE"
    REASSIGNMENT = "REASSIGNMENT"


@dataclass(frozen=True)
class OverrideMetadata:
    admin_id: str
    reason_text: str
    timestamp: str  # ISO8601


@dataclass(frozen=True)
class AssignmentPolicy:
    source: AssignmentSource
    reason: AssignmentReason
    override: Optional[OverrideMetadata] = None
