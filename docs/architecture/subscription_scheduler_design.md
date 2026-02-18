BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Subscription Scheduler Design

## Scope
Abonelik yenileme/iptal akışı ile weekly planner entegrasyonunu tanımlar.

## Owners
- Scheduling Lead
- Backend Architect

## Last updated
2026-02-18

## SSOT references
- KR-015
- KR-033

## Design overview
- Subscription lifecycle: active -> renewal_due -> renewed | canceled.
- Planner integration: yenilenen abonelikler weekly planning kuyruğuna düşer.
- İptal veya payment reject durumunda planlama isteği geri çekilir.

## Capacity relation (KR-015)
- Scheduler, weekly planner’a yalnızca kapasite-kontrollü talep gönderir.
- Aşırı yoğunlukta seed/pull kotaları ve yeniden planlama tokenları devrededir.
- Büyük alan talepleri çoklu pilot atamasına yönlendirilir.

## Operate
- Günlük iş dağıtımı scheduler job’ı ile tetiklenir.
- Admin override süreli ve audit kayıtlıdır.
- Weather block durumunda görevler “hold” statüsüne alınır.

## Observability
- `scheduler_renewal_jobs_total`
- `planner_queue_depth`
- `reschedule_token_usage_total`

## Failure modes
- Renewal yarış durumu -> idempotent geçiş.
- Planner downtime -> retry + dead-letter queue.
- Kapasite aşımı -> defer + operator alarmı.

## Checklists
### Preflight
- Yenileme tetik kuralları güncel.
- Planner sözleşmesi doğrulandı.

### Operate
- Queue derinliği ve gecikme izleniyor.
- Override işlemleri auditleniyor.

### Postmortem
- Kapasite ihlali analizi tamamlandı.
- Kural ve eşikler revize edildi.

## Related docs
- `docs/views/VIEW_CAPABILITIES.md`
- `docs/runbooks/weather_block_verification_procedure.md`
- `docs/KR-033_payment_flow.md`
