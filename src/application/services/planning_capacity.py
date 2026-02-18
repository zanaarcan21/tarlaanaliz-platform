# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: "dönüm → efor → kapasite" hesaplarını standardize etmek.
Sorumluluk: Use-case orkestrasyonu; domain service + ports birleşimi; policy enforcement.
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


class CapacityError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class CapacityPlan:
    area_donum: float
    effort_points: float
    required_pilots: int


@dataclass(slots=True)
class PlanningCapacityService:
    effort_per_donum: float = 1.0
    max_daily_effort_per_pilot: float = 200.0

    def calculate(self, *, area_donum: float) -> CapacityPlan:
        if area_donum <= 0:
            raise CapacityError("area_donum_must_be_positive")

        effort_points = area_donum * self.effort_per_donum
        required_pilots = max(1, int(-(-effort_points // self.max_daily_effort_per_pilot)))

        # KR-015: kapasite planlaması kontrollü hesap ile standardize edilir.
        return CapacityPlan(
            area_donum=area_donum,
            effort_points=effort_points,
            required_pilots=required_pilots,
        )
