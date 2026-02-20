/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Pilot Settings" };

export default function PilotSettingsPage() {
  return (
    <section className="space-y-4" aria-label="Pilot settings" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Pilot Ayarları</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">Bildirim ve tercih ayarları (stub).</div>
    </section>
  );
}
