/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Admin Experts" };

export default function AdminExpertsPage() {
  return (
    <section className="space-y-4" aria-label="Admin experts" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Expert Yönetimi</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">Aktif expert: 26 · Onay bekleyen: 3</div>
    </section>
  );
}
