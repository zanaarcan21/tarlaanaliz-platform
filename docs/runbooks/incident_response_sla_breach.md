BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Incident Response: SLA Breach

## Scope
SLA ihlalinin sınıflandırılması, mitigasyon ve kalıcı düzeltme adımlarını tanımlar.

## Owners
- Incident Commander
- SRE Lead
- Service Owner

## Last updated
2026-02-18

## SSOT references
- KR-015
- KR-033

## Measurement & classification
- Sev-1: kritik ödeme/planlama akışları etkilenir.
- Sev-2: kısmi gecikme, geri kazanım mümkün.
- Sev-3: sınırlı etki, kullanıcı etkisi düşük.

## Mitigation steps
1. Etkilenen endpointleri daralt.
2. Rate limit profilini adaptif moda al.
3. Gerekirse düşük öncelikli iş yükünü shed et.
4. Kritik iş akışlarını priorite et.

## Permanent fix
- Kök neden analizi -> kod/konfig değişikliği.
- Alarm eşiklerinin güncellenmesi.
- Runbook revizyonu.

## Observability
- `sla_breach_open_total`
- `sla_recovery_minutes`
- `p95_endpoint_latency`

## Checklists
### Preflight
- SLA tanımları ve eşikler güncel.
- On-call rota doğrulandı.

### Operate
- İhlal sınıfı atandı.
- Mitigasyon aksiyonları zaman damgalı kaydedildi.

### Postmortem
- Kalıcı aksiyon sahipleri atandı.
- İlgili dokümanlar güncellendi.

## Related docs
- `docs/api/openapi.yaml`
- `docs/architecture/adaptive_rate_limiting.md`
- `docs/security/ddos_mitigation_plan.md`
