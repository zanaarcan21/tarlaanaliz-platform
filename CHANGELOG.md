# Changelog

Tum onemli degisiklikler bu dosyada belgelenir.
Format [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standardina,
surumleme [SemVer](https://semver.org/) politikasina uyar.

SSOT Referansi: `docs/TARLAANALIZ_SSOT_v1_0_0.txt` — KR-000 surumleme politikasi.

## [Unreleased]

### Added

- Proje iskelet yapisi (scaffold) olusturuldu (v3.2.2 agac yapisi)
- SSOT v1.0.0 dokumani eklendi (`docs/TARLAANALIZ_SSOT_v1_0_0.txt`)
- LLM Brief v1.0.0 eklendi (`docs/TARLAANALIZ_LLM_BRIEF_v1_0_0.md`)
- Playbook v1.0.0 eklendi (`docs/TARLAANALIZ_PLAYBOOK_v1_0_0.md`)
- Clean Architecture katman yapisi: `src/core/`, `src/application/`, `src/infrastructure/`, `src/presentation/`
- CQRS pattern: commands + queries ayriligi
- Domain entities: User, Field, Mission, Pilot, Expert, Subscription, PaymentIntent, AnalysisJob
- Value objects: ParcelRef, Geometry, Money, MissionStatus, ConfidenceScore, CropType, Province, Role
- Domain events: Field, Mission, Payment, Subscription, Analysis, Expert lifecycle olaylari
- Domain services: CalibrationValidator, CapacityManager, MissionPlanner, PricebookCalculator, SLAMonitor
- Repository ports: 20+ repository interface tanimi
- External ports: PaymentGateway, SMSGateway, StorageService, ParcelGeometryProvider, EventBus
- Infrastructure adapters: SQLAlchemy, Redis, RabbitMQ, S3/MinIO, Cloudflare, TKGM/MEGSIS
- Alembic migration framework: 16 migration sablonu
- FastAPI endpoint iskeletleri: 15+ endpoint
- Frontend (Next.js) feature modules: subscriptions, results, expert-portal, weather-block, training-feedback
- i18n destek yapisi: tr, ar, ku
- Test scaffolding: unit, integration, e2e, performance

## [3.2.2] - 2026-02-08

### Added

- Baslangic surumu; platform tree v3.2.2 FINAL olarak sabitlendi
- KR-033 PaymentIntent tablolari ve odeme akisi migration'i
- KR-082 Kalibrasyon ve QC kayit tablolari migration'i
- WeatherBlockReport tablolari migration'i
- Frontend CI workflow (build + lint + e2e)

### Security

- KR-040/KR-041 SDLC kapilari tanimla ndi
- KR-050 Telefon + PIN kimlik modeli belirlendi
- KR-063 RBAC matrisi (12 rol) dokumante edildi
- KR-066 PII ayriligi kurallari belirlendi
- KR-070 YZ izolasyonu ve tek yonlu akis politikasi belirlendi
