BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Security Plan: DDoS Mitigation

## Scope
Katmanlı DDoS azaltım stratejisini (edge, app, runtime) ve operasyon adımlarını tanımlar.

## Owners
- Security Lead
- SRE Lead

## Last updated
2026-02-18

## SSOT references
- KR-081
- KR-033

## Layered controls
- Edge: WAF/CDN tabanlı temel filtreleme (vendor-agnostic).
- API: endpoint bazlı rate limit + adaptive mode.
- Runtime: circuit breaker, queue backpressure, load shedding.

## Operational steps
1. Saldırı tipini sınıflandır.
2. Edge kural setini sıkılaştır.
3. Uygulama limit profillerini yükselt.
4. Kritik endpointlere kapasite rezerv et.
5. Olay süresince telemetry ve audit topla.

## Metrics & alerts
- `ddos_suspected_requests_total`
- `waf_block_ratio`
- `api_429_ratio`
- `critical_endpoint_error_rate`

## Failure modes
- False block of legitimate traffic.
- Aşırı agresif limit nedeniyle SLA ihlali.
- Edge bypass pattern.

## Checklists
### Preflight
- DDoS politika profilleri hazır.
- Kritik endpoint listesi güncel.

### Operate
- Saldırı sınıfı ve uygulanan profil kaydedildi.
- Mitigasyon etkisi metriklerle doğrulandı.

### Postmortem
- Kural seti tuning yapıldı.
- Incident raporu ve aksiyonlar kapatıldı.

## Related docs
- `docs/architecture/adaptive_rate_limiting.md`
- `docs/runbooks/incident_response_sla_breach.md`
- `docs/api/openapi.yaml`
