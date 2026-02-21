// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { useMemo } from 'react';

function generateId(prefix: string) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function useCorrelationId(seed?: string) {
  const corrId = useMemo(() => seed ?? generateId('corr'), [seed]);

  const createRequestId = () => generateId('req');

  const withTraceHeaders = (headers?: HeadersInit, requestId?: string): HeadersInit => ({
    ...(headers ?? {}),
    'x-corr-id': corrId,
    'x-request-id': requestId ?? createRequestId()
  });

  return {
    corrId,
    createRequestId,
    withTraceHeaders
  };
}
