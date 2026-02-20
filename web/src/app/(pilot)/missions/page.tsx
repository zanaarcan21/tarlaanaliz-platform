/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Pilot Missions" };

export default function PilotMissionsPage() {
  return (
    <section className="space-y-4" aria-label="Pilot missions" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Görevlerim</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">Bugün için 2 görev atandı.</div>
    </section>
  );
}
