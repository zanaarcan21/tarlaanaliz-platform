BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

# Title
VIEW: 3D Grouping (Domain × SDLC × Deployment)

## Scope
Sistemi üç eksende özetleyen kavramsal görünümü sunar.

## Owners
- Platform Architect
- Technical Writer

## Last updated
2026-02-18

## SSOT references
- KR-018
- KR-033
- KR-081

## Dimension 1: Domain
- Payment lifecycle
- Calibration & QC
- Planning & scheduling
- Expert review & feedback
- SLA observability

## Dimension 2: SDLC stage
- Plan
- Build
- Test
- Deploy
- Operate

## Dimension 3: Deployment node
- API node (`src/presentation/api`)
- Worker node (queue consumers)
- AI isolated node (KR-071)
- Observability node

## Mapping notes
- Payment domain operasyonu deploy/operate ekseninde KR-033 gate ile izlenir.
- Calibration/QC domaini test/deploy ekseninde KR-018 gate ile izlenir.
- Contract yönetimi build/test ekseninde KR-081 ile doğrulanır.

## Checklists
### Preflight
- Domain haritası güncel.
- Node sorumlulukları ayrıştırıldı.

### Operate
- Domain bazlı alarm panelleri aktif.
- Eksenler arası sahiplik net.

### Postmortem
- Görünümde eksik alanlar güncellendi.
- Yeni capability’ler eşlendi.

## Related docs
- `docs/views/VIEW_CAPABILITIES.md`
- `docs/views/VIEW_SDLC.md`
