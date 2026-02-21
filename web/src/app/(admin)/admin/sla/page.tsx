/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Admin SLA",
};

export default function AdminSlaPage() {
  return (
    <section className="space-y-4" aria-label="Admin SLA dashboard" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">SLA İzleme</h1>
      <ul className="list-inside list-disc rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <li>İnceleme başlangıç SLA: &lt; 2 saat</li>
        <li>Karar SLA: &lt; 24 saat</li>
        <li>Mevcut uyum: %96</li>
      </ul>
    </section>
  );
}
