/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Queue contract tipleri ile fetch edilir. */
/* KR-071: corr_id/request_id izleri request metadata olarak taşınır. */

import { useCallback, useEffect, useMemo, useState } from "react";

import { apiRequest } from "../../../lib/apiClient";
import type { CorrelationMeta, ExpertQueueItem, ExpertQueueStats } from "../types";

interface QueueResponse {
  readonly items: readonly ExpertQueueItem[];
}

export interface UseExpertQueueResult extends CorrelationMeta {
  readonly items: readonly ExpertQueueItem[];
  readonly stats: ExpertQueueStats;
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly refetch: () => Promise<void>;
}

function computeStats(items: readonly ExpertQueueItem[]): ExpertQueueStats {
  return {
    total: items.length,
    queued: items.filter((item) => item.status === "queued").length,
    inReview: items.filter((item) => item.status === "in_review").length,
    completed: items.filter((item) => item.status === "completed").length,
  };
}

export function useExpertQueue(): UseExpertQueueResult {
  const [items, setItems] = useState<readonly ExpertQueueItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [corrId, setCorrId] = useState("-");
  const [requestId, setRequestId] = useState("-");

  const fetchQueue = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiRequest<QueueResponse>("/api/expert/queue", { method: "GET" });
      setItems(response.data.items);
      setCorrId(response.corrId);
      setRequestId(response.requestId);
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : "Queue load failed");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchQueue();
  }, [fetchQueue]);

  return useMemo(
    () => ({
      items,
      stats: computeStats(items),
      isLoading,
      error,
      refetch: fetchQueue,
      corrId,
      requestId,
    }),
    [corrId, error, fetchQueue, isLoading, items, requestId]
  );
}
