BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Incident Response: Payment Timeout

## Scope
Payment intent/receipt/onay hattında timeout olayının tespiti, triage ve düzeltme adımlarını tanımlar.

## Owners
- Incident Commander
- Payments Ops
- Backend On-Call

## Last updated
2026-02-18

## SSOT references
- KR-033
- KR-081

## Detection
- Alarm: payment işlem gecikmesi eşiği aşıldı.
- Sinyaller: queue lag artışı, approval latency artışı.

## Triage
1. Etki kapsamı: hangi payment state’ler etkilendi?
2. İdempotent tekrar güvenli mi kontrol et.
3. Bağımlı servis sağlık durumlarını doğrula.

## Technical actions
- Kuyruk tüketicisini yeniden ölçekle.
- Takılan işlemleri correlation id ile yeniden oynat.
- Çakışan state geçişlerinde conflict guard uygula.

## Customer communication template (short)
- “Ödeme işleminizde gecikme tespit edildi. Kaydınız korunuyor; manuel doğrulama sonrası bilgilendirme yapılacaktır.”

## Postmortem focus
- Timeout kök nedeni (altyapı/iş kuralı/entegrasyon).
- Tekrarını engelleyecek aksiyonlar.

## Checklists
### Preflight
- Alarm eşiği ve rota bilgisi güncel.
- İletişim şablonu hazır.

### Operate
- Etkilenen payment_id listesi çıkarıldı.
- Geri kazanım adımları auditlendi.

### Postmortem
- Olay zaman çizelgesi tamamlandı.
- Kalıcı düzeltme backlog’a işlendi.

## Related docs
- `docs/KR-033_payment_flow.md`
- `docs/api/openapi.yaml`
- `docs/runbooks/payment_approval_procedure.md`
