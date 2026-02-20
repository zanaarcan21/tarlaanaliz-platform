/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Admin Pricing",
};

export default function AdminPricingPage() {
  return (
    <section className="space-y-4" aria-label="Admin pricing management" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Fiyat Yönetimi</h1>
      <p className="text-sm text-slate-600">Fiyat setleri backend hazır olduğunda typed client ile bağlanacaktır.</p>
      <div className="rounded-lg border border-slate-200 bg-white p-4">
        <p className="font-medium">Plan: Standard</p>
        <p className="text-sm text-slate-600">Durum: Taslak</p>
      </div>
    </section>
  );
}
