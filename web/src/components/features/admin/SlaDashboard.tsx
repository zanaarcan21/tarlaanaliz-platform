// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
export interface SlaKpi {
  key: string;
  label: string;
  value: number;
  target: number;
  unit?: string;
}

interface SlaDashboardProps {
  items: SlaKpi[];
}

export function SlaDashboard({ items }: SlaDashboardProps) {
  return (
    <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4" data-testid="sla-dashboard">
      {items.map((item) => {
        const healthy = item.value <= item.target;
        return (
          <article key={item.key} className="rounded-lg border border-slate-200 bg-white p-4">
            <p className="text-sm text-slate-600">{item.label}</p>
            <p className="mt-1 text-2xl font-semibold text-slate-900">
              {item.value}
              {item.unit ? <span className="ml-1 text-sm text-slate-500">{item.unit}</span> : null}
            </p>
            <p className={`mt-2 text-xs font-medium ${healthy ? 'text-emerald-700' : 'text-rose-700'}`}>
              Target: {item.target}
              {item.unit ?? ''}
            </p>
          </article>
        );
      })}
    </div>
  );
}
