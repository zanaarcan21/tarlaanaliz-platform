# PATH: src/infrastructure/monitoring/__init__.py
# DESC: Infrastructure monitoring package: sağlık kontrolü, metrikler, güvenlik logları.
"""
Infrastructure monitoring adapters.

Amaç: Python paket başlangıcı; modül dışa aktarım (exports) ve namespace düzeni.
Sorumluluk: Python paket başlangıcı; import yüzeyini (public API) düzenler.
Notlar/SSOT: KR-015, KR-018, KR-033, KR-081 ile tutarlı kalır.
"""

from src.infrastructure.monitoring.health_checks import (
    CheckResult,
    HealthChecker,
    HealthReport,
    HealthStatus,
)
from src.infrastructure.monitoring.prometheus_metrics import (
    PrometheusMetrics,
    get_metrics,
)
from src.infrastructure.monitoring.security_events import (
    SecurityCategory,
    SecurityEventLogger,
    SecuritySeverity,
)

__all__: list[str] = [
    # Health checks
    "CheckResult",
    "HealthChecker",
    "HealthReport",
    "HealthStatus",
    # Prometheus metrics
    "PrometheusMetrics",
    "get_metrics",
    # Security events
    "SecurityCategory",
    "SecurityEventLogger",
    "SecuritySeverity",
]
