# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.  # noqa: RUF003
# KR-081: Field CRUD orchestration uses explicit contract models and ports.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class Field:
    field_id: str
    owner_user_id: str
    name: str
    parcel_ref: str | None = None
    geometry_wkt: str | None = None


class FieldRepository(Protocol):
    def create(self, field: Field) -> None: ...

    def get(self, field_id: str) -> Field | None: ...

    def update(self, field: Field) -> None: ...

    def delete(self, field_id: str) -> None: ...


class EventBus(Protocol):
    def publish(self, event_name: str, payload: dict[str, Any], *, correlation_id: str) -> None: ...


class FieldService:
    def __init__(self, repo: FieldRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def create_field(self, *, field: Field, correlation_id: str) -> None:
        self._repo.create(field)
        self._bus.publish(
            "field.created",
            {"field_id": field.field_id, "owner_user_id": field.owner_user_id},
            correlation_id=correlation_id,
        )

    def update_field(self, *, field: Field, correlation_id: str) -> None:
        self._repo.update(field)
        self._bus.publish("field.updated", {"field_id": field.field_id}, correlation_id=correlation_id)

    def delete_field(self, *, field_id: str, correlation_id: str) -> None:
        self._repo.delete(field_id)
        self._bus.publish("field.deleted", {"field_id": field_id}, correlation_id=correlation_id)
