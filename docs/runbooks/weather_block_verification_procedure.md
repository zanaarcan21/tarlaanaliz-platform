BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Runbook: Weather Block Verification Procedure

## Scope
Uçuş/planlama engeli (weather block) durumunda doğrulama, false positive yönetimi ve audit adımlarını tanımlar.

## Owners
- Flight Ops Lead
- Scheduler Ops

## Last updated
2026-02-18

## SSOT references
- KR-015

## Verification procedure
1. Bloklanan görevleri listele.
2. Veri kaynağı zaman damgasını doğrula.
3. Bölgesel tutarlılık kontrolü yap.
4. Gerekirse manuel ikinci doğrulama uygula.
5. Sonucu planner’a (hold/release) yansıt.

## False positive handling
- Kısa süreli anomalide bekleme penceresi uygula.
- Çelişkili veri varsa manuel override + audit zorunlu.

## Audit fields
- mission_id
- block_source
- verification_result
- operator_subject_id
- correlation_id

## Failure modes
- Stale weather data.
- Yanlış bölge eşleşmesi.
- Override kaydının atlanması.

## Checklists
### Preflight
- Veri kaynağı erişimi sağlıklı.
- Planner entegrasyonu aktif.

### Operate
- Blok/release kararları loglandı.
- False positive oranı izlendi.

### Postmortem
- Hatalı blok kararları analiz edildi.
- Eşikler ve doğrulama adımı güncellendi.

## Related docs
- `docs/architecture/subscription_scheduler_design.md`
- `docs/views/VIEW_CAPABILITIES.md`
