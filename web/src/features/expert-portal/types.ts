/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Contract-first tip tanımları. */

export type QueueItemStatus = "queued" | "in_review" | "completed";

export interface ExpertQueueItem {
  readonly reviewId: string;
  readonly missionId: string;
  readonly fieldName: string;
  readonly priority: "low" | "medium" | "high";
  readonly status: QueueItemStatus;
  readonly createdAtIso: string;
}

export interface ExpertQueueStats {
  readonly total: number;
  readonly queued: number;
  readonly inReview: number;
  readonly completed: number;
}

export interface ExpertReviewDetail {
  readonly reviewId: string;
  readonly missionId: string;
  readonly notes: string;
  readonly createdAtIso: string;
  readonly updatedAtIso: string;
}

export interface CorrelationMeta {
  readonly corrId: string;
  readonly requestId: string;
}
