/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Expert Settings",
};

export default function ExpertSettingsPage() {
  return (
    <section className="space-y-4" aria-label="Expert settings" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Ayarlar</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <p>Bildirim sesi: Açık</p>
        <p>Varsayılan bant görünümü: NDVI</p>
      </div>
    </section>
  );
}
