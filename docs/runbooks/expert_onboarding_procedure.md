BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Runbook: Expert Onboarding Procedure

## Scope
Uzman hesabı aktivasyonu, rol ataması ve ilk görev hazırlığını işletim adımlarıyla tanımlar.

## Owners
- Expert Ops Lead
- Security Operations

## Last updated
2026-02-18

## SSOT references
- KR-081
- KR-071

## Procedure
1. Onboarding talebini ticket sistemi üzerinden doğrula.
2. Kimlik/rol doğrulamasını tamamla.
3. RBAC rolünü ata (`expert` / `reviewer`).
4. İlk görev havuzuna kontrollü erişim ver.
5. Audit event üret ve ticket’a bağla.

## Rollback
- Yanlış rol ataması: erişimi kaldır, oturumları sonlandır.
- Şüpheli aktivite: hesap kilitle, security incident aç.

## Verify
- Uzman yalnız yetkili endpointlere erişebilmeli.
- İlk görev ataması SLA içi gerçekleşmeli.

## Failure modes
- Yetki fazlalığı -> anında role downgrade.
- Eksik audit kaydı -> manuel reconciliation.

## Checklists
### Preflight
- Onboarding talebi onaylı.
- Rol matrisi güncel.

### Operate
- Aktivasyon süresi ve hata oranı takipte.
- Audit kaydı üretildi.

### Postmortem
- İhlal veya hata varsa kök neden yazıldı.
- Süreç adımı güncellendi.

## Related docs
- `docs/architecture/expert_portal_design.md`
- `docs/security/model_protection_strategy.md`
