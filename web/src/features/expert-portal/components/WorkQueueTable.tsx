/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Queue tablo satırları tipli contract ile taşınır. */

import { formatDateTime } from "../../../lib/date";
import type { ExpertQueueItem } from "../types";

export interface WorkQueueTableProps {
  readonly items: readonly ExpertQueueItem[];
  readonly onOpen: (reviewId: string) => void;
  readonly corrId?: string;
  readonly requestId?: string;
}

export function WorkQueueTable({ items, onOpen, corrId, requestId }: WorkQueueTableProps) {
  return (
    <div className="overflow-x-auto" data-corr-id={corrId} data-request-id={requestId}>
      <table className="min-w-full border-collapse" aria-label="Expert iş kuyruğu tablosu">
        <thead>
          <tr className="border-b text-left">
            <th className="p-2">Review</th>
            <th className="p-2">Mission</th>
            <th className="p-2">Tarla</th>
            <th className="p-2">Öncelik</th>
            <th className="p-2">Durum</th>
            <th className="p-2">Tarih</th>
            <th className="p-2">Aksiyon</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td colSpan={7} className="p-3 text-sm text-slate-500">
                Kayıt bulunamadı.
              </td>
            </tr>
          ) : (
            items.map((item) => (
              <tr key={item.reviewId} className="border-b">
                <td className="p-2">{item.reviewId}</td>
                <td className="p-2">{item.missionId}</td>
                <td className="p-2">{item.fieldName}</td>
                <td className="p-2">{item.priority}</td>
                <td className="p-2">{item.status}</td>
                <td className="p-2">{formatDateTime(item.createdAtIso)}</td>
                <td className="p-2">
                  <button type="button" onClick={() => onOpen(item.reviewId)} className="rounded border px-2 py-1">
                    Aç
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
