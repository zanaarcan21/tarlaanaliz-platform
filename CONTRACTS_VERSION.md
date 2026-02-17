# Contracts Version — Surum Sabitleme (Pinning)

> **KR-081** Contract-First: Backend, Frontend ve Worker ayni API/Event semasini
> konustugunun garantisi bu dosya ile saglanir.

## Aktif Contract Surumu

| Alan | Deger |
|------|-------|
| **Contract Set Version** | `1.0.0` |
| **Schema Draft** | JSON Schema draft 2020-12 |
| **SSOT Referansi** | `docs/TARLAANALIZ_SSOT_v1_0_0.txt` — KR-081 |
| **Checksum Dosyasi** | `CONTRACTS_SHA256.txt` |
| **Son Guncelleme** | 2026-02-08 |

## Contract Listesi

| Contract | Schema ID | Surum | Durum |
|----------|-----------|-------|-------|
| AnalysisJob | `analysis_job.v1` | 1.0.0 | Aktif |
| AnalysisResult | `analysis_result.v1` | 1.0.0 | Aktif |
| AI Feedback | `ai.feedback.v1` | 1.0.0 | Aktif |
| Training Export (CLS) | `training.feedback.cls.v1` | 1.0.0 | Aktif |
| Training Export (GEO) | `training.feedback.geo.v1` | 1.0.0 | Aktif |

## Surumleme Kurali (SemVer)

- **v1.x**: Geriye uyumlu (backward compatible) eklemeler serbest (optional field eklenebilir)
- **v2.0**: Breaking change; bu dosya + `CONTRACTS_SHA256.txt` zorunlu guncellenir
- Breaking change tespit edildiginde CI pipeline merge'u engeller (KR-041)

## Uyumluluk Matrisi

| Servis | Minimum Contract Version | Notlar |
|--------|--------------------------|--------|
| Backend (Platform) | 1.0.0 | Uretici + tuketici |
| AI Worker | 1.0.0 | Tuketici (AnalysisJob) + uretici (AnalysisResult) |
| Frontend (PWA) | 1.0.0 | Tuketici (AnalysisResult) |
| Edge Kiosk | 1.0.0 | Uretici (ingest manifest) |
