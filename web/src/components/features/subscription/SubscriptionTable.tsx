// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
export interface SubscriptionRow {
  id: string;
  planName: string;
  startDate: string;
  endDate: string;
  status: 'active' | 'pending' | 'cancelled';
}

interface SubscriptionTableProps {
  rows: SubscriptionRow[];
}

const statusClass: Record<SubscriptionRow['status'], string> = {
  active: 'bg-emerald-100 text-emerald-800',
  pending: 'bg-amber-100 text-amber-800',
  cancelled: 'bg-rose-100 text-rose-800'
};

export function SubscriptionTable({ rows }: SubscriptionTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200" data-testid="subscription-table">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 text-left text-slate-600">
          <tr>
            <th className="px-3 py-2">Plan</th>
            <th className="px-3 py-2">Başlangıç</th>
            <th className="px-3 py-2">Bitiş</th>
            <th className="px-3 py-2">Durum</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-t border-slate-100">
              <td className="px-3 py-2 text-slate-900">{row.planName}</td>
              <td className="px-3 py-2 text-slate-700">{new Date(row.startDate).toLocaleDateString('tr-TR')}</td>
              <td className="px-3 py-2 text-slate-700">{new Date(row.endDate).toLocaleDateString('tr-TR')}</td>
              <td className="px-3 py-2">
                <span className={`rounded-full px-2 py-1 text-xs font-medium ${statusClass[row.status]}`}>{row.status}</span>
              </td>
            </tr>
          ))}
          {rows.length === 0 ? (
            <tr>
              <td colSpan={4} className="px-3 py-6 text-center text-slate-500">
                Abonelik kaydı bulunamadı.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}
