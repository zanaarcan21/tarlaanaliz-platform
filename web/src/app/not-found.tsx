/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

import Link from "next/link";

export default function NotFoundPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col items-center justify-center gap-3 px-4 text-center">
      <h1 className="text-3xl font-semibold">404</h1>
      <p className="text-sm text-slate-600">Aradığınız sayfa bulunamadı.</p>
      <Link href="/" className="rounded bg-slate-900 px-4 py-2 text-sm text-white">
        Ana Sayfa
      </Link>
    </main>
  );
}
