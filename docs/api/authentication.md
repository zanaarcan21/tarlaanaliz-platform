BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Authentication & Authorization (Phone + PIN, JWT)

## Scope
`src/presentation/api` yüzeyindeki kimlik doğrulama ve yetkilendirme modelini tanımlar.

## Owners
- Backend Lead
- Security Engineer
- API Product Owner

## Last updated
2026-02-18

## SSOT references
- KR-033
- KR-081

## Identity flow (high level)
- Kimlik doğrulama yöntemi: phone + PIN.
- JWT içinde doğrulanmış subject kimliği taşınır (`sub`).
- PII minimizasyonu gereği phone/PIN/token loglanmaz.

## Token model
- Access token: kısa ömürlü, API erişimi için.
- Refresh token: döndürmeli kullanım, ihlal durumunda iptal edilebilir.
- Claims (örnek): `sub`, `role`, `scope`, `iat`, `exp`, `jti`.

## Public endpoints
- `GET /health`
- Kimlik üretim/yenileme endpointleri (bu dokümanda örneklenir, OpenAPI kapsamı servis sınırına göre tutulur).

## RBAC & permissions
- Farmer:
  - payment intent oluşturma
  - kendi payment durumunu görüntüleme
  - receipt yükleme
- Admin:
  - pending payment listeleme
  - approve/reject aksiyonları
- Expert:
  - review/feedback akışlarında yetkili işlemler (ayrı modül).

## PII redaction rules
- Telefon numarası: `+90*******45`
- JWT: `[REDACTED_TOKEN]`
- PIN: hiçbir log seviyesinde tutulmaz.

## Example cURL (masked)
```bash
curl -X POST https://api.example.local/v1/payments/intents \
  -H "Authorization: Bearer [REDACTED_TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"subject_id":"usr_123","plan_code":"pilot_standard","amount":1250.00,"currency":"TRY"}'
```

## Example masked log
```text
ts=2026-02-18T10:02:11Z level=INFO event=auth.accepted subject=usr_123 phone=+90*******45 token=[REDACTED_TOKEN]
```

## Verification points
- JWT doğrulama middleware’i yalnızca `src/presentation/api` altında kullanılmalı.
- Role -> endpoint matrisi otomatik test ile doğrulanmalı.
- Yetkisiz erişim 401/403 dönmeli.

## Failure modes
- Expired token -> 401.
- Invalid scope -> 403.
- Replay şüphesi (jti çakışması) -> token revocation + audit event.

## Checklists
### Preflight
- Claim sözlüğü güncel.
- Role izin matrisi güncel.
- Masking kuralları log pipeline’da aktif.

### Operate
- 401/403 oranları dashboard’da izleniyor.
- Refresh başarısızlıkları alarm eşiğine bağlı.

### Postmortem
- İhlal olayında jti/sub bazlı audit çıkartıldı.
- Redaction ihlali varsa pipeline kuralı güncellendi.

## Related docs
- `docs/api/openapi.yaml`
- `docs/security/ddos_mitigation_plan.md`
- `docs/runbooks/incident_response_sla_breach.md`
