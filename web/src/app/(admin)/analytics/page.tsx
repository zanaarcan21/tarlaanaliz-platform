/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: corr/request trace bilgileri UI metadata alanlarında taşınır. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Admin Analytics",
};

const metricCards = [
  { label: "Toplam Analiz", value: "1,284" },
  { label: "Aktif Expert", value: "26" },
  { label: "Bekleyen İnceleme", value: "74" },
  { label: "SLA Uyum", value: "%96" },
] as const;

export default function AdminAnalyticsPage() {
  return (
    <section aria-label="Admin analytics" data-corr-id="pending" data-request-id="pending" className="space-y-6">
      <h1 className="text-2xl font-semibold">Analytics</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metricCards.map((card) => (
          <article key={card.label} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-600">{card.label}</p>
            <p className="mt-1 text-2xl font-bold text-slate-900">{card.value}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
