/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Admin Users",
};

export default function AdminUsersPage() {
  return (
    <section className="space-y-4" aria-label="Admin users" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Kullanıcı Yönetimi</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
        <p>Toplam kullanıcı: 1,042</p>
        <p>Aktif roller: admin / expert / farmer / pilot</p>
      </div>
    </section>
  );
}
