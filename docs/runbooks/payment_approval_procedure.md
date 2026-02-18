BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Runbook: Payment Manual Approval Procedure

## Scope
Admin tarafındaki manuel ödeme onay/reddetme sürecini ve doğrulama kontrollerini tanımlar.

## Owners
- Payments Operations
- Fraud Analyst
- Admin Support Lead

## Last updated
2026-02-18

## SSOT references
- KR-033
- KR-081

## Approval procedure
1. Payment intent varlığını doğrula.
2. Receipt bütünlüğünü ve uygunluğunu doğrula.
3. Şüpheli sinyal kontrolü yap.
4. Approve veya reject kararı ver.
5. Audit kaydını zorunlu üret.

## Fraud signals (examples)
- Yinelenen dekont hash.
- Tutarsız tutar/currency.
- Kısa sürede çoklu intent + receipt pattern.

## Audit requirements
- actor_subject_id
- action (approve/reject)
- reason_code
- correlation_id
- timestamp

## Failure modes
- Race condition: aynı payment için çift karar.
- Eksik receipt metadata.
- Yetkisiz admin aksiyonu.

## Checklists
### Preflight
- Pending listesi güncel çekildi.
- Fraud sinyal kuralları aktif.

### Operate
- Her karar için reason_code girildi.
- Audit event doğrulandı.

### Postmortem
- Hatalı karar vakaları analiz edildi.
- Kural seti güncellendi.

## Related docs
- `docs/KR-033_payment_flow.md`
- `docs/api/openapi.yaml`
- `docs/runbooks/incident_response_payment_timeout.md`
