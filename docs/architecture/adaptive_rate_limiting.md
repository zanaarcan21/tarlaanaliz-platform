BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Adaptive Rate Limiting Strategy

## Scope
API katmanında sabit + adaptif oran sınırlama yaklaşımı, yük dökme ve izleme modelini tanımlar.

## Owners
- Platform Architect
- SRE Lead
- Security Engineer

## Last updated
2026-02-18

## SSOT references
- KR-033
- KR-081

## Why
- Trafik patlamalarında servis sürekliliği sağlamak.
- Hassas endpointlerde kötüye kullanım riskini azaltmak.

## How
- Baseline: token bucket (global) + sliding window (endpoint).
- Adaptif mod tetikleri:
  - 5xx oran artışı
  - belirli endpointte ani RPS artışı
  - anomali skor eşiği aşımı
- Tetiklenince:
  - burst limit düşürülür
  - retry-after başlığı zorunlu döner
  - düşük öncelikli endpointlerde load shedding uygulanır

## Operate
- Allowlist: internal health/ops aktörleri.
- Admin override: süreli ve audit kayıtlı.
- Payment ve approval endpointleri için daha sıkı limit profili.

## Observability
- `http_requests_limited_total{endpoint}`
- `http_retry_after_seconds{endpoint}`
- `adaptive_mode_active{profile}`
- `error_rate_5xx{endpoint}`

## Failure modes
- False positive throttling -> override + profil geri alma.
- Redis/cache kaybı -> güvenli fallback (statik limit).
- Load shedding aşırı agresif -> SLO alarmı ve profil tuning.

## Pseudo-config
```yaml
rate_limit:
  default:
    token_bucket_rps: 50
    burst: 100
  endpoints:
    /v1/admin/payments/pending:
      sliding_window_rpm: 30
  adaptive:
    enabled: true
    trigger_5xx_ratio: 0.03
    retry_after_seconds: 30
```

## Checklists
### Preflight
- Limit profilleri endpoint kritikliğine göre güncel.
- Retry-After başlığı test edildi.

### Operate
- 429 oranı ve 5xx korelasyonu izleniyor.
- Adaptive mod aç/kapa olayları auditleniyor.

### Postmortem
- Yanlış limit olayında eşikler revize edildi.
- İlgili runbook aksiyonları güncellendi.

## Related docs
- `docs/security/ddos_mitigation_plan.md`
- `docs/api/openapi.yaml`
- `docs/runbooks/incident_response_sla_breach.md`
