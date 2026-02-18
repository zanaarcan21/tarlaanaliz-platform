# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Bekleyen expert review listesi.
Sorumluluk: Read use-case (CQRS query): RBAC, filtreleme/pagination, projection/DTO üretimi.
Girdi/Çıktı (Contract/DTO/Event): Girdi: API/Job/Worker tetiklemesi. Çıktı: DTO, event, state transition.
Güvenlik (RBAC/PII/Audit): RBAC burada; PII redaction; audit log; rate limit (gereken yerde).
Hata Modları (idempotency/retry/rate limit): 400/403/409/429/5xx mapping; retry-safe tasarım; idempotency key/hard gate’ler.
Observability (log fields/metrics/traces): correlation_id, latency, error_code; use-case metric sayaçları.
Testler: Unit + integration; kritik akış için e2e (özellikle ödeme/planlama/kalibrasyon).
Bağımlılıklar: Domain + ports + infra implementasyonları + event bus.
Notlar/SSOT: Contract-first (KR-081) ve kritik kapılar (KR-018/KR-033/KR-015) application katmanında enforce edilir.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, Protocol, TypeVar


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Page(Generic[T]):
    items: tuple[T, ...]
    page: int
    page_size: int
    total: int


class QueryAuthzError(PermissionError):
    pass


class QueryRateLimitError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ListPendingExpertReviewsRequest:
    actor_user_id: str
    correlation_id: str
    page: int = 1
    page_size: int = 20


@dataclass(frozen=True, slots=True)
class PendingExpertReviewItem:
    review_id: str
    mission_id: str
    analysis_result_id: str
    assigned_at: datetime
    status: str


@dataclass(frozen=True, slots=True)
class ListPendingExpertReviewsResult:
    correlation_id: str
    page: Page[PendingExpertReviewItem]


class PendingExpertReviewReadPort(Protocol):
    async def list_pending(self, *, page: int, page_size: int) -> tuple[list[PendingExpertReviewItem], int]: ...


class AuthorizerPort(Protocol):
    async def can_list_pending_expert_reviews(self, actor_user_id: str) -> bool: ...


class RateLimiterPort(Protocol):
    async def allow(self, *, actor_user_id: str, action: str) -> bool: ...


class AuditLoggerPort(Protocol):
    async def log_query(self, *, correlation_id: str, actor_user_id: str, query_name: str) -> None: ...


@dataclass(slots=True)
class ListPendingExpertReviewsQuery:
    read_port: PendingExpertReviewReadPort
    authorizer: AuthorizerPort
    rate_limiter: RateLimiterPort
    audit_logger: AuditLoggerPort

    async def execute(self, request: ListPendingExpertReviewsRequest) -> ListPendingExpertReviewsResult:
        if request.page <= 0 or request.page_size <= 0:
            raise ValueError("page and page_size must be positive")

        if not await self.rate_limiter.allow(actor_user_id=request.actor_user_id, action="list_pending_expert_reviews"):
            raise QueryRateLimitError("rate limit exceeded")
        if not await self.authorizer.can_list_pending_expert_reviews(request.actor_user_id):
            raise QueryAuthzError("actor is not authorized")

        items, total = await self.read_port.list_pending(page=request.page, page_size=request.page_size)
        await self.audit_logger.log_query(
            correlation_id=request.correlation_id,
            actor_user_id=request.actor_user_id,
            query_name="ListPendingExpertReviewsQuery",
        )
        return ListPendingExpertReviewsResult(
            correlation_id=request.correlation_id,
            page=Page(items=tuple(items), page=request.page, page_size=request.page_size, total=total),
        )
