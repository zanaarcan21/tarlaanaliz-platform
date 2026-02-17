# Güncellenecek (Overwrite edilmeyen) dosyalar

Aşağıdaki dosyalar dokümanda **[GÜNCELLEME]** olarak geçiyor; repo'nuzda zaten varsa
üzerine yazmak riskli olduğu için bu pakette *değiştirmedim*.

## KR-015 güncellemeleri

- `src/core/domain/entities/subscription.py`
  - `plan_type = SEASONAL`
  - `reschedule_tokens_per_season` (int)
  - `reschedule_tokens_remaining` (int)

- `src/core/domain/entities/mission.py`
  - `schedule_window_start`, `schedule_window_end`
  - `assignment_source` (SYSTEM_SEED | PULL)
  - `assignment_reason` (AUTO_DISPATCH | ADMIN_OVERRIDE | REASSIGNMENT)

- `src/core/domain/entities/pilot.py`
  - `work_days` (max 6 gün/hafta)
  - `daily_capacity_donum` (2500–3000)
  - `system_seed_quota_donum` (varsayılan 1500)
  - `reliability_score`

- `src/application/services/subscription_scheduler.py`
  - “season schedule preview” üretimi
  - reschedule sonrası `next_due_at` yeniden hesap
  - upcoming window listesi → `auto_dispatcher` beslemesi

- `src/infrastructure/persistence/models/subscription_model.py`
  - token alanları + `plan_type`

- `src/infrastructure/persistence/repositories/subscription_repository.py`
  - schedule preview sorguları

## Not
İstersen bir sonraki adımda, bu dosyaları da **mevcut içeriklerini görerek** (senin repodan)
safe-diff şeklinde patch’leyebiliriz.
