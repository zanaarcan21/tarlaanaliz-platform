// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
interface ResultMetric {
  label: string;
  value: string;
}

export interface ResultDetail {
  id: string;
  title: string;
  capturedAt: string;
  description: string;
  metrics: ResultMetric[];
  requestId?: string;
  corrId?: string;
}

interface ResultDetailPanelProps {
  detail?: ResultDetail;
}

export function ResultDetailPanel({ detail }: ResultDetailPanelProps) {
  if (!detail) {
    return <section className="rounded-lg border border-slate-200 p-4 text-sm text-slate-500">Detay seçilmedi.</section>;
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4" data-testid="result-detail-panel" data-request-id={detail.requestId} data-corr-id={detail.corrId}>
      <h3 className="text-lg font-semibold text-slate-900">{detail.title}</h3>
      <p className="mt-1 text-xs text-slate-500">{new Date(detail.capturedAt).toLocaleString('tr-TR')}</p>
      <p className="mt-3 text-sm text-slate-700">{detail.description}</p>
      <dl className="mt-4 grid grid-cols-2 gap-2 text-sm">
        {detail.metrics.map((metric) => (
          <div key={metric.label} className="rounded-md bg-slate-50 p-2">
            <dt className="text-slate-500">{metric.label}</dt>
            <dd className="font-medium text-slate-900">{metric.value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
