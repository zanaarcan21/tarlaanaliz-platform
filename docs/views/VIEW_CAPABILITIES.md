BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
VIEW: Platform Capabilities

## Scope
Ana ürün kabiliyetlerini giriş/çıkış/sınır/KR referansı ile listeler.

## Owners
- Product Architect
- Platform Owner

## Last updated
2026-02-18

## SSOT references
- KR-015
- KR-018
- KR-033
- KR-081

## Capability map
### Calibration & QC gate
- Input: mission payload, calibration record, QC report
- Output: analysis eligibility signal
- Boundary: gate geçmeden analysis başlatılmaz
- KR: KR-018

### Payment processing
- Input: payment intent, receipt
- Output: approved/paid veya rejected state
- Boundary: manuel onay + audit zorunlu
- KR: KR-033

### Weekly planning
- Input: subscription demand, field workload, weather signal
- Output: weekly assignments, reschedule actions
- Boundary: kapasite ve çoklu pilot kuralı
- KR: KR-015

### Expert review
- Input: analysis artifacts
- Output: reviewed labels, feedback events
- Boundary: RBAC + audit
- KR: KR-081, KR-071

### SLA dashboard
- Input: latency/error/event telemetry
- Output: breach summary, breach list
- Boundary: observability veri bütünlüğü
- KR: KR-081

## Checklists
### Preflight
- Capability sınırları güncel.
- Giriş/çıkış alanları API contract ile uyumlu.

### Operate
- Capability bazlı metrikler izleniyor.
- Sınır ihlalleri alarmlanıyor.

### Postmortem
- Yeni öğrenimler capability haritasına işlendi.
- Sahiplikler güncellendi.

## Related docs
- `docs/api/openapi.yaml`
- `docs/architecture/subscription_scheduler_design.md`
- `docs/KR-033_payment_flow.md`
