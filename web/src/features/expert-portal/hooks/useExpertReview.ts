/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Review detail contract-first tip ile yüklenir. */
/* KR-071: corr_id/request_id izleri request metadata olarak taşınır. */

import { useCallback, useEffect, useState } from "react";

import { apiRequest } from "../../../lib/apiClient";
import type { CorrelationMeta, ExpertReviewDetail } from "../types";

interface ReviewResponse {
  readonly item: ExpertReviewDetail;
}

export interface UseExpertReviewResult extends CorrelationMeta {
  readonly review: ExpertReviewDetail | null;
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly refetch: () => Promise<void>;
}

export function useExpertReview(reviewId: string): UseExpertReviewResult {
  const [review, setReview] = useState<ExpertReviewDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [corrId, setCorrId] = useState("-");
  const [requestId, setRequestId] = useState("-");

  const fetchReview = useCallback(async () => {
    if (!reviewId) {
      setReview(null);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await apiRequest<ReviewResponse>(`/api/expert/reviews/${encodeURIComponent(reviewId)}`, {
        method: "GET",
      });
      setReview(response.data.item);
      setCorrId(response.corrId);
      setRequestId(response.requestId);
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : "Review load failed");
    } finally {
      setIsLoading(false);
    }
  }, [reviewId]);

  useEffect(() => {
    void fetchReview();
  }, [fetchReview]);

  return {
    review,
    isLoading,
    error,
    refetch: fetchReview,
    corrId,
    requestId,
  };
}
