/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Queue verisi contract-first tiplerle render edilir. */

import type { Metadata } from "next";
import Link from "next/link";

import type { ExpertQueueItem } from "../../../features/expert-portal/types";

export const metadata: Metadata = {
  title: "Expert Queue",
};

const queueItems: readonly ExpertQueueItem[] = [
  {
    reviewId: "rvw_001",
    missionId: "msn_1001",
    fieldName: "Deneme Tarlası A",
    priority: "high",
    status: "queued",
    createdAtIso: "2026-02-20T09:00:00.000Z",
  },
];

export default function ExpertQueuePage() {
  return (
    <section className="space-y-4" aria-label="Expert queue" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">İnceleme Kuyruğu</h1>
      <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
        <table className="min-w-full text-left text-sm">
          <thead className="border-b bg-slate-50">
            <tr>
              <th className="p-3">Review</th>
              <th className="p-3">Mission</th>
              <th className="p-3">Tarla</th>
              <th className="p-3">Öncelik</th>
              <th className="p-3">Aksiyon</th>
            </tr>
          </thead>
          <tbody>
            {queueItems.map((item) => (
              <tr key={item.reviewId} className="border-b last:border-0">
                <td className="p-3">{item.reviewId}</td>
                <td className="p-3">{item.missionId}</td>
                <td className="p-3">{item.fieldName}</td>
                <td className="p-3">{item.priority}</td>
                <td className="p-3">
                  <Link href={`/review/${item.reviewId}`} className="rounded border px-2 py-1 text-xs hover:bg-slate-50">
                    Aç
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
