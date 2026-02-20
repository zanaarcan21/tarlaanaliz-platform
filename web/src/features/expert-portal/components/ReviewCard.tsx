/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Review kartı contract-first veri modeli ile taşınır. */

export interface ReviewCardData {
  readonly reviewId: string;
  readonly missionId: string;
  readonly fieldName: string;
  readonly createdAtIso: string;
  readonly status: "queued" | "in_review" | "completed";
}

export interface ReviewCardProps {
  readonly data: ReviewCardData;
  readonly onOpen: (reviewId: string) => void;
  readonly corrId?: string;
  readonly requestId?: string;
}

export function ReviewCard({ data, onOpen, corrId, requestId }: ReviewCardProps) {
  return (
    <article
      className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
      aria-label={`İnceleme kartı ${data.reviewId}`}
      data-corr-id={corrId}
      data-request-id={requestId}
    >
      <header className="mb-3">
        <h3 className="text-base font-semibold">{data.fieldName}</h3>
        <p className="text-sm text-slate-600">Mission: {data.missionId}</p>
      </header>
      <dl className="mb-4 text-sm">
        <div>
          <dt className="inline font-medium">Durum: </dt>
          <dd className="inline">{data.status}</dd>
        </div>
        <div>
          <dt className="inline font-medium">Oluşturulma: </dt>
          <dd className="inline">{new Date(data.createdAtIso).toLocaleString("tr-TR")}</dd>
        </div>
      </dl>
      <button type="button" onClick={() => onOpen(data.reviewId)} className="rounded border px-3 py-2">
        İncelemeyi Aç
      </button>
    </article>
  );
}
