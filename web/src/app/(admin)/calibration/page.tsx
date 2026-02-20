/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-018: kalibrasyon hard-gate görünürlüğü. */

import type { Metadata } from "next";

export const metadata: Metadata = { title: "Admin Calibration" };

export default function AdminCalibrationPage() {
  return (
    <section className="space-y-4" aria-label="Admin calibration" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Kalibrasyon İzleme</h1>
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm">Kalibrasyon bekleyen görev: 5</div>
    </section>
  );
}
