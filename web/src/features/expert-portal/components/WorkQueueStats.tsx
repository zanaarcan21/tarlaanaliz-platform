/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Queue stats contract-first prop ile taşınır. */

import type { ExpertQueueStats } from "../types";

export interface WorkQueueStatsProps {
  readonly stats: ExpertQueueStats;
  readonly corrId?: string;
  readonly requestId?: string;
}

export function WorkQueueStats({ stats, corrId, requestId }: WorkQueueStatsProps) {
  return (
    <section aria-label="İş kuyruğu istatistikleri" data-corr-id={corrId} data-request-id={requestId}>
      <ul className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <li className="rounded border p-3">
          <p className="text-xs text-slate-600">Toplam</p>
          <p className="text-lg font-semibold">{stats.total}</p>
        </li>
        <li className="rounded border p-3">
          <p className="text-xs text-slate-600">Kuyrukta</p>
          <p className="text-lg font-semibold">{stats.queued}</p>
        </li>
        <li className="rounded border p-3">
          <p className="text-xs text-slate-600">İncelemede</p>
          <p className="text-lg font-semibold">{stats.inReview}</p>
        </li>
        <li className="rounded border p-3">
          <p className="text-xs text-slate-600">Tamamlanan</p>
          <p className="text-lg font-semibold">{stats.completed}</p>
        </li>
      </ul>
    </section>
  );
}
