// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
export interface AuditLogRow {
  id: string;
  actor: string;
  action: string;
  createdAt: string;
  requestId?: string;
  corrId?: string;
}

interface AuditLogTableProps {
  rows: AuditLogRow[];
}

export function AuditLogTable({ rows }: AuditLogTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200" data-testid="audit-log-table">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 text-left text-slate-600">
          <tr>
            <th className="px-3 py-2">Actor</th>
            <th className="px-3 py-2">Action</th>
            <th className="px-3 py-2">Timestamp</th>
            <th className="px-3 py-2">Trace</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-t border-slate-100">
              <td className="px-3 py-2 text-slate-900">{row.actor}</td>
              <td className="px-3 py-2 text-slate-700">{row.action}</td>
              <td className="px-3 py-2 text-slate-700">{new Date(row.createdAt).toLocaleString('tr-TR')}</td>
              <td className="px-3 py-2 text-xs text-slate-500">
                <span className="block">req: {row.requestId ?? '-'}</span>
                <span className="block">corr: {row.corrId ?? '-'}</span>
              </td>
            </tr>
          ))}
          {rows.length === 0 ? (
            <tr>
              <td colSpan={4} className="px-3 py-6 text-center text-slate-500">
                Audit kaydı bulunamadı.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}
