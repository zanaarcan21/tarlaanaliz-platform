# TarlaAnaliz Platform

Tarimsal drone goruntu analizi platformu. Ciftcilerin urun kaybini erken uyari ile azaltmak
ve donum bazli analiz hizmeti sunmak icin gelistirilen backend + frontend monorepo'su.

> **SSOT:** `docs/TARLAANALIZ_SSOT_v1_0_0.txt` — Tek kanonik kaynak. Tum kurallar bu dokumana referansla uygulanir.

## Ozellikler

- **Tarla Yonetimi** — Ciftci/kooperatif tarla kaydi, TKGM/MEGSIS parsel entegrasyonu [KR-013]
- **Drone Gorev Planlama** — DJI Mavic 3M ile KMZ gorev dosyasi uretimi [KR-016]
- **YZ Analizi** — Izole, tek yonlu akisla bitki sagligi analizi (NDVI/NDRE) [KR-017]
- **Radyometrik Kalibrasyon** — Hard gate: kalibrasyonsuz veri islenmez [KR-018/082]
- **Uzman Inceleme** — Dusuk guven skorlu sonuclarda expert portal [KR-019]
- **Abonelik Sistemi** — Sezonluk otomatik mission planlama [KR-027]
- **Odeme Yonetimi** — Kredi karti + IBAN/EFT, manuel onay akisi [KR-033]
- **RBAC** — 12 rol ile yetki matrisi, PII ayriligi [KR-063]
- **Harita Katmanlari** — 7 katman: saglik, hastalik, zararli, mantar, yabanci ot, su/azot stresi [KR-002]

## Teknoloji Yigini

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic |
| Frontend | Next.js 14, TypeScript, Tailwind CSS, PWA |
| Veritabani | PostgreSQL 16 + PostGIS |
| Cache | Redis 7 |
| Mesaj Kuyrugu | RabbitMQ 3.13 |
| Object Storage | S3 / MinIO |
| CI/CD | GitHub Actions |
| Container | Docker, docker-compose |

## Hizli Baslangic

### Gereksinimler

- Docker ve Docker Compose
- Python 3.12+ (yerel gelistirme icin)
- Node.js 20+ ve pnpm (frontend icin)

### Kurulum

```bash
# 1. Repo'yu klonla
git clone <repo-url> tarlaanaliz-platform
cd tarlaanaliz-platform

# 2. Cevre degiskenlerini ayarla
cp .env.example .env
# .env dosyasini duzenle

# 3. Docker ile tum servisleri baslat
docker-compose up -d

# 4. Veritabani migration'larini calistir
docker-compose exec backend alembic upgrade head

# 5. Seed data yukle (opsiyonel)
docker-compose exec backend python scripts/seed_data.py
```

### Yerel Gelistirme (Docker'siz)

```bash
# Python ortami
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Pre-commit hook'larini kur
pre-commit install

# Backend'i baslat
uvicorn src.presentation.api.main:app --reload --port 8000

# Frontend'i baslat (ayri terminal)
cd web && pnpm install && pnpm dev
```

## Proje Yapisi

```
tarlaanaliz-platform/
├── src/                  Backend (Clean Architecture)
│   ├── core/domain/      Domain: entities, value objects, events, ports
│   ├── application/      Use cases: commands, queries, DTOs, services
│   ├── infrastructure/   Adapters: DB, cache, MQ, external APIs
│   └── presentation/     API endpoints (FastAPI) + CLI
├── web/                  Frontend (Next.js PWA)
├── alembic/              DB migration'lari
├── tests/                Test suite
├── docs/                 SSOT + mimari dokumanlar
├── config/               Runtime konfigurasyon
└── scripts/              Yardimci scriptler
```

## Test

```bash
# Tum testleri calistir
pytest

# Sadece unit testler
pytest tests/unit -m unit

# Integration testler (Docker servisleri gerekli)
pytest tests/integration -m integration

# Coverage raporu
pytest --cov=src --cov-report=html
```

## SSOT ve Dokumantasyon

| Dokuman | Aciklama |
|---------|----------|
| `docs/TARLAANALIZ_SSOT_v1_0_0.txt` | Tek kanonik kaynak (BAGLAYICI) |
| `docs/TARLAANALIZ_LLM_BRIEF_v1_0_0.md` | Gelistirici rehberi |
| `docs/TARLAANALIZ_PLAYBOOK_v1_0_0.md` | Operasyonel playbook |
| `AGENTS.md` | AI agent kodlama kurallari |
| `CONTRACTS_VERSION.md` | Contract surum sabitleme |
| `CHANGELOG.md` | Surum notlari |
| `MANIFEST_CANONICAL.md` | Proje manifest ozeti |

## Katki

1. AGENTS.md dosyasini okuyun — kodlama kurallari burada
2. Her dosyanin basinda SSOT header'i bulunmalidir
3. Is kurallari KR kodu ile referanslanir, tekrar yazilmaz
4. Contract-first yaklasim: schema/interface once, implementasyon sonra
5. PR'larda KR-041 SDLC kapilari uygulanir

## Lisans

Proprietary — TarlaAnaliz
