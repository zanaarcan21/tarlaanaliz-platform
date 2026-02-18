# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
"""
Amaç: Contract-first (KR-081) JSON Schema doğrulaması.
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
from typing import Any, Protocol



class JsonSchemaPort(Protocol):
    def validate(self, *, schema_name: str, payload: dict[str, Any]) -> None: ...


@dataclass(slots=True)
class ContractValidatorService:
    schema_port: JsonSchemaPort

    def validate_payload(self, *, schema_name: str, payload: dict[str, Any]) -> None:
        # KR-081: contract-first doğrulama, orkestrasyon başlamadan önce uygulanır.
        self.schema_port.validate(schema_name=schema_name, payload=payload)
