BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Expert Portal Design (High Level)

## Scope
Uzman onboarding, görev atama, review ve feedback loop akışının üst-seviye mimarisini tanımlar.

## Owners
- Product Architect
- Expert Ops Lead
- Security Lead

## Last updated
2026-02-18

## SSOT references
- KR-081
- KR-071

## Module boundaries
- Onboarding: uzman profil doğrulama ve yetki atama.
- Assignment: görev havuzundan uzman atama.
- Review: kalite inceleme ve etiketleme.
- Feedback: model geliştirme hattına kontrollü geri besleme.

## Security model
- RBAC zorunlu (expert/reviewer/admin).
- Tüm kritik aksiyonlar audit event üretir.
- PII minimizasyonu uygulanır.

## Operate
- Queue-based assignment ile yoğunluk yönetilir.
- SLA kritik görevler öncelikli kuyrukta işlenir.
- Reassignment işlemleri auditlenir.

## Observability
- `expert_assignment_latency_seconds`
- `review_backlog_count`
- `feedback_acceptance_ratio`

## Failure modes
- Uzman kapasite düşüşü -> otomatik yeniden atama.
- Yanlış rol ataması -> erişim iptali + audit inceleme.
- Review backlog artışı -> kapasite uyarısı.

## Checklists
### Preflight
- Role matrisi güncel.
- Assignment politikası doğrulandı.

### Operate
- Backlog ve SLA metrikleri izleniyor.
- Kritik aksiyonlar audit dashboard’da görünür.

### Postmortem
- Hatalı atama kök neden analizi tamamlandı.
- Süreç kuralı ve eğitim notları güncellendi.

## Related docs
- `docs/architecture/training_feedback_architecture.md`
- `docs/runbooks/expert_onboarding_procedure.md`
- `docs/security/model_protection_strategy.md`
