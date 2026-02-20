/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-033: ödeme/onay adımlarında audit görünürlüğü. */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Admin Audit",
};

export default function AdminAuditPage() {
  return (
    <section aria-label="Admin audit logs" className="space-y-4" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Audit Logları</h1>
      <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
        <table className="min-w-full text-left text-sm">
          <thead className="border-b bg-slate-50">
            <tr>
              <th className="p-3">Zaman</th>
              <th className="p-3">Kullanıcı</th>
              <th className="p-3">İşlem</th>
              <th className="p-3">Durum</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b">
              <td className="p-3">2026-02-20 10:41</td>
              <td className="p-3">admin_01</td>
              <td className="p-3">payment.manual_approval</td>
              <td className="p-3">success</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}
