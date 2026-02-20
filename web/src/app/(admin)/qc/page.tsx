/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: QC çıktıları contract-first doğrulama adımlarına bağlanır. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Admin QC" };

export default function AdminQcPage() {
  return (
    <section className="space-y-4" aria-label="Admin quality control" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">QC Kontrol</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">QC kuyruğu ve doğrulama adımları (stub).</div>
    </section>
  );
}
