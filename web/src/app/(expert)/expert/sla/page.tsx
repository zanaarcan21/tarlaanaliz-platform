/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Expert SLA",
};

export default function ExpertSlaPage() {
  return (
    <section className="space-y-4" aria-label="Expert SLA" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">SLA Durumu</h1>
      <ul className="list-inside list-disc rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <li>Ortalama ilk yanıt: 1 saat 12 dk</li>
        <li>Açık işlerin SLA riski: 3</li>
      </ul>
    </section>
  );
}
