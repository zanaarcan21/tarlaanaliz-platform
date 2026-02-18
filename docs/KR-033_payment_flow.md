BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
KR-033 Reference: Payment Flow

## Scope
Ödeme durum makinesi, audit event seti, idempotency ve yarış durumu yönetimini özetler.

## Owners
- Payments Domain Lead
- Backend Architect

## Last updated
2026-02-18

## SSOT references
- KR-033
- KR-081

## State machine
- `intent_created`
- `receipt_uploaded`
- `pending_manual_approval`
- terminal:
  - `approved` -> `paid`
  - `rejected`

## Transition rules
- intent yoksa paid geçişi yok.
- receipt olmadan pending_manual_approval yok.
- approve/reject yalnız admin role.
- tüm geçişlerde audit event zorunlu.

## Audit events (minimum)
- `payment.intent.created`
- `payment.receipt.uploaded`
- `payment.approval.pending`
- `payment.approved`
- `payment.rejected`
- `payment.paid`

## Idempotency
- `idempotency_key` create/upload işlemlerinde zorunlu önerilir.
- Aynı key ile tekrar çağrılar aynı state sonucunu döner.

## Race conditions
- Parallel approve/reject çağrıları:
  - optimistic lock veya state version kontrolü.
  - ikinci işlem `409 Conflict` döner.
- Duplicate receipt upload:
  - hash veya key ile dedupe.

## Example response (minimal)
```json
{
  "payment_id": "pay_456",
  "subject_id": "usr_123",
  "state": "pending_manual_approval",
  "audit_ref": "aud_789"
}
```

## Checklists
### Preflight
- State geçiş matrisi güncel.
- Idempotency davranışı testli.

### Operate
- Pending kuyruğu ve approval latency izleniyor.
- Conflict oranı takip ediliyor.

### Postmortem
- Hatalı geçiş olayları analiz edildi.
- Guard kuralları güncellendi.

## Related docs
- `docs/api/openapi.yaml`
- `docs/runbooks/payment_approval_procedure.md`
- `docs/runbooks/incident_response_payment_timeout.md`
