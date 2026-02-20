/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Route param ve response contract-first tiplerle ele alınır. */
/* KR-071: corr/request metadata response ile taşınır. */

import type { Metadata } from "next";

import { apiRequest } from "../../../../lib/apiClient";
import type { ExpertReviewDetail } from "../../../../features/expert-portal/types";

interface ReviewPageParams {
  readonly reviewId: string;
}

interface ReviewPageProps {
  readonly params: ReviewPageParams;
}

interface ReviewResponse {
  readonly item: ExpertReviewDetail;
}

export const metadata: Metadata = {
  title: "Expert Review",
};

export default async function ExpertReviewDetailPage({ params }: ReviewPageProps) {
  const reviewId = params.reviewId;

  let review: ExpertReviewDetail | null = null;
  try {
    const response = await apiRequest<ReviewResponse>(`/api/expert/reviews/${encodeURIComponent(reviewId)}`, {
      method: "GET",
    });
    review = response.data.item;
  } catch {
    review = null;
  }

  return (
    <section aria-label="Expert review detail" className="space-y-4" data-corr-id="pending" data-request-id="pending">
      <h1 className="text-2xl font-semibold">Review Detayı</h1>
      {review ? (
        <article className="rounded-lg border border-slate-200 bg-white p-4 text-sm">
          <p>Review ID: {review.reviewId}</p>
          <p>Mission ID: {review.missionId}</p>
          <p>Not: {review.notes}</p>
        </article>
      ) : (
        <p className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm">Detay verisi henüz alınamadı.</p>
      )}
    </section>
  );
}
