# TarlaAnaliz Platform — Canonical Manifest

> **SSOT Uyumlu:** `docs/TARLAANALIZ_SSOT_v1_0_0.txt` v1.0.0
> **Platform Tree:** v3.2.2 FINAL (2026-02-08)

## Proje Ozeti

**Amac:** Ciftcilerin urun kaybini erken uyari ile azaltmak ve donum bazli analiz hizmeti satmak.
Baslangic bolgesi GAP, ardindan Turkiye geneline olcekleme. **[KR-001]**

**Sabit Cerceve:**
- Drone: DJI Mavic 3M
- Veri: RGB + multispektral (NDVI/NDRE)
- YZ sadece analiz yapar; ilaclama/gubreleme karari **VERMEZ**
- Sonuclar PWA uygulamasinda harita uzerinde renk + desen/ikon ile gosterilir

## SSOT Dokuman Seti

| Dokuman | Yol | Tip |
|---------|-----|-----|
| Kanonik SSOT | `docs/TARLAANALIZ_SSOT_v1_0_0.txt` | Normatif (BAGLAYICI) |
| LLM Brief | `docs/TARLAANALIZ_LLM_BRIEF_v1_0_0.md` | Gelistirici rehberi |
| Playbook | `docs/TARLAANALIZ_PLAYBOOK_v1_0_0.md` | Operasyonel (bilgilendirici) |
| Platform Tree | `docs/tarlaanaliz_platform_tree_v3.2.2_FINAL_2026-02-08.txt` | Yapisal referans |
| Is Plani | `docs/IS_PLANI_AKIS_DOKUMANI_v1_0_0.docx` | Is akisi |

## Mimari Ozet

```
Presentation (FastAPI + CLI + PWA)
    |
Application (CQRS: Commands + Queries + DTOs + Event Handlers)
    |
Domain (Entities + Value Objects + Events + Services + Ports)
    |
Infrastructure (SQLAlchemy + Redis + RabbitMQ + S3 + External Adapters)
```

**Pattern:** Clean Architecture + CQRS + Event-Driven Design

## Temel KR Referanslari

| KR | Baslik | Aciklama |
|----|--------|----------|
| KR-001 | Proje Ozeti | Kapsam ve sabit cerceve |
| KR-013 | Ciftci Uyeligi | Tarla kaydi tekilligi |
| KR-015 | Pilot Kapasitesi | work_days <= 6, daily_capacity_donum |
| KR-017 | YZ Izolasyonu | Tek yonlu akis, inbound yok |
| KR-018/082 | Kalibrasyon | Hard gate: kalibrasyonsuz analiz yok |
| KR-019 | Expert Portal | Confidence threshold + uzman inceleme |
| KR-022 | Fiyat Yonetimi | PriceBook snapshot, immutable |
| KR-027 | Subscription Scheduler | Sezonluk otomatik mission uretimi |
| KR-033 | Odeme Akisi | Manuel onay + audit log |
| KR-040/041 | SDLC Kapilari | PR/CI/Release/Ops guvenligi |
| KR-050 | Kimlik | Telefon + 6 haneli PIN |
| KR-063 | RBAC | 12 rol yetki matrisi |
| KR-066 | KVKK/PII | PII ayriligi |
| KR-081 | Contract-First | JSON Schema machine-verifiable |

## Repo Yapisi (Ust Duzey)

```
tarlaanaliz-platform/
├── .github/workflows/    CI/CD pipeline'lari
├── alembic/              DB migration'lari (16 versiyon)
├── config/               Runtime konfigurasyon (rate limits, logging)
├── docs/                 SSOT + mimari + runbook + guvenlik dokumanlari
├── scripts/              Yardimci scriptler (seed, backup, export)
├── src/                  Backend kaynak kodu (Python/FastAPI)
│   ├── application/      Use cases (CQRS)
│   ├── core/domain/      Domain katmani (entities, VO, events, ports)
│   ├── infrastructure/   Adapter'lar (DB, cache, MQ, external)
│   └── presentation/     API endpoints + CLI
├── tests/                Test suite (unit, integration, e2e, performance)
└── web/                  Frontend (Next.js 14 + TypeScript + PWA)
```

## Servis Bagimliliklari

| Servis | Gorevi | Port (dev) |
|--------|--------|------------|
| PostgreSQL + PostGIS | Ana veritabani | 5432 |
| Redis | Cache + rate limiting | 6379 |
| RabbitMQ | Event bus + job queue | 5672 / 15672 |
| MinIO | Object storage (S3) | 9000 / 9001 |
| Backend (FastAPI) | API + business logic | 8000 |
| Frontend (Next.js) | PWA web uygulamasi | 3000 |

## Contract Surumu

- **Aktif:** v1.0.0 (bkz. `CONTRACTS_VERSION.md`)
- **Checksum:** `CONTRACTS_SHA256.txt`
- **Surumleme:** SemVer (KR-081)
