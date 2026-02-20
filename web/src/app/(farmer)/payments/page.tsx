/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-033: ödeme + manuel onay + audit akışı görünür tutulur. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Farmer Payments",
};

export default function FarmerPaymentsPage() {
  return (
    <section className="space-y-4" aria-label="Farmer payments" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Ödemeler</h1>
      <article className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <p>Durum: Manual onay bekliyor</p>
        <p>Dekont: yüklendi</p>
      </article>
    </section>
  );
}
