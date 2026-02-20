/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Farmer Subscriptions",
};

export default function FarmerSubscriptionsPage() {
  return (
    <section className="space-y-4" aria-label="Farmer subscriptions" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Abonelikler</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <p>Plan: Sezonluk</p>
        <p>Durum: Aktif</p>
      </div>
    </section>
  );
}
