/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-015: pilot kapasite/planlama görünürlüğü yönetim ekranında tutulur. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Admin Pilots" };

export default function AdminPilotsPage() {
  return (
    <section className="space-y-4" aria-label="Admin pilots" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Pilot Yönetimi</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">Kapasite raporları ve atama ekranı (stub).</div>
    </section>
  );
}
