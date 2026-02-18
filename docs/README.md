BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
Docs Directory Guide (Living Documentation)

## Scope
Bu dosya `docs/` altındaki bilgi mimarisini, güncelleme akışını ve PR doğrulama yaklaşımını tanımlar.

## Owners
- Staff Backend Architect
- Technical Writer
- Platform Owner

## Last updated
2026-02-18

## SSOT references
- KR-015
- KR-018
- KR-033
- KR-081

## How to read this docs set
1. Önce `docs/TARLAANALIZ_SSOT_v1_0_0.txt` okunur.
2. Sonra `docs/views/` ile sistem resmi görülür.
3. `docs/architecture/` ile tasarım kararları doğrulanır.
4. `docs/api/` ile contract seviyesi kontrol edilir.
5. `docs/runbooks/` ile işletim prosedürleri çalıştırılır.
6. `docs/security/` ile risk ve koruma önlemleri doğrulanır.

## Documentation classes
- `docs/api/`: API contract, auth, endpoint davranışları.
- `docs/architecture/`: katman, event, scheduler ve portal kararları.
- `docs/runbooks/`: operasyon adımları, incident prosedürleri.
- `docs/security/`: DDoS ve model koruma stratejileri.
- `docs/views/`: üst-seviye sistem görünümleri.
- `docs/KR-033_payment_flow.md`: ödeme durum akışı referansı.

## Living docs principles
- Karar metni yerine KR referansı kullanılır.
- Contract-first yaklaşımı korunur (KR-081).
- Operasyonel prosedürler gözlemlenebilir metriklerle ilişkilendirilir.
- Doküman değişikliği kod/contract değişikliği ile aynı PR içinde yapılır.

## Docs update flow
- Değişiklik tetikleyicisi: endpoint, şema, runbook veya güvenlik kontrolü değişimi.
- Etki analizi: ilgili KR ve bağlı dokümanlar listelenir.
- Güncelleme: dosya başlığı meta alanları + içerik + checklist.
- Doğrulama: örnek istek/yanıt, olay akışı, observability alanları.

## PR checklist (docs)
- İlgili KR referansları eklendi mi?
- API adları `docs/api/openapi.yaml` ile tutarlı mı?
- PII redaction örnekleri maskeli mi?
- Runbook adımları rollback/postmortem içeriyor mu?
- Related docs listesi güncellendi mi?

## Checklists
### Preflight
- SSOT sürümü doğrulandı.
- Etkilenen dosyalar haritalandı.
- Terminoloji tutarlılığı kontrol edildi.

### Operate
- Değişiklik sonrası endpoint/şema örnekleri doğrulandı.
- Runbook ve security doküman bağlantıları doğrulandı.

### Postmortem
- Yanlış veya eksik kural referansı varsa düzeltildi.
- Gelecek güncelleme için açık aksiyonlar kaydedildi.

## Related docs
- `docs/TARLAANALIZ_SSOT_v1_0_0.txt`
- `docs/api/openapi.yaml`
- `docs/views/VIEW_SDLC.md`
- `docs/KR-033_payment_flow.md`
