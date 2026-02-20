/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: İzlenebilirlik için correlation/request id üretimi. */

export interface CorrelationIds {
  readonly corrId: string;
  readonly requestId: string;
}

function randomPart(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function createCorrelationId(prefix = "corr"): string {
  return `${prefix}_${randomPart()}`;
}

export function createRequestId(prefix = "req"): string {
  return `${prefix}_${randomPart()}`;
}

export function createCorrelationIds(): CorrelationIds {
  return {
    corrId: createCorrelationId(),
    requestId: createRequestId(),
  };
}

export function toCorrelationHeaders(ids: Partial<CorrelationIds>): Record<string, string> {
  const headers: Record<string, string> = {};
  if (ids.corrId) {
    headers["x-corr-id"] = ids.corrId;
  }
  if (ids.requestId) {
    headers["x-request-id"] = ids.requestId;
  }
  return headers;
}
