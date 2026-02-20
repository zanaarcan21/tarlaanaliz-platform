/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: hata yüzeyinde trace metadata taşınır. */

"use client";

interface GlobalErrorProps {
  readonly error: Error & { digest?: string };
  readonly reset: () => void;
}

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  return (
    <html lang="tr">
      <body>
        <main className="mx-auto flex min-h-screen max-w-2xl flex-col items-center justify-center gap-4 px-4 text-center">
          <h1 className="text-2xl font-semibold">Beklenmeyen Hata</h1>
          <p className="text-sm text-slate-600" data-corr-id={error.digest ?? "unknown"} data-request-id="error-boundary">
            İşlem sırasında bir hata oluştu.
          </p>
          <button type="button" onClick={reset} className="rounded bg-slate-900 px-4 py-2 text-sm text-white">
            Tekrar Dene
          </button>
        </main>
      </body>
    </html>
  );
}
