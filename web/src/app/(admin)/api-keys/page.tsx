/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: key yönetim ekranında trace metadata görünür. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Admin API Keys" };

export default function AdminApiKeysPage() {
  return (
    <section className="space-y-4" aria-label="Admin API keys" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">API Anahtarları</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">Anahtar listesi ve rotasyon aksiyonları (stub).</div>
    </section>
  );
}
