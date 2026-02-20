/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-018: Kalibrasyonsuz analiz çıktısı listelenmez. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Farmer Results",
};

export default function FarmerResultsPage() {
  return (
    <section className="space-y-4" aria-label="Farmer results" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Sonuçlar</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <p>Mission #msn_1001 · NDVI raporu hazır</p>
      </div>
    </section>
  );
}
