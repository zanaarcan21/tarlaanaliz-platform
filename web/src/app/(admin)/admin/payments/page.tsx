/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-033: payment + manuel onay + audit akışı zorunlu görünürlük. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Admin Payments" };

export default function AdminPaymentsPage() {
  return (
    <section className="space-y-4" aria-label="Admin payments" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Ödeme İnceleme</h1>
      <article className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <p>PaymentIntent: pi_001</p>
        <p>Dekont: mevcut</p>
        <p>Manuel onay: bekliyor</p>
      </article>
    </section>
  );
}
