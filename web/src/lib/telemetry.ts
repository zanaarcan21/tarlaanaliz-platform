/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: Observability eventleri corr/request id ile taşınır. */

import { createCorrelationIds } from "./correlation";

export interface TelemetryEvent {
  readonly name: string;
  readonly corrId?: string;
  readonly requestId?: string;
  readonly metadata?: Record<string, string | number | boolean | null>;
}

export type TelemetrySink = (event: Required<Omit<TelemetryEvent, "metadata">> & {
  readonly metadata: Record<string, string | number | boolean | null>;
  readonly ts: string;
}) => void;

let sink: TelemetrySink | null = null;

export function registerTelemetrySink(nextSink: TelemetrySink): void {
  sink = nextSink;
}

export function trackEvent(event: TelemetryEvent): void {
  const ids = createCorrelationIds();
  const payload = {
    name: event.name,
    corrId: event.corrId ?? ids.corrId,
    requestId: event.requestId ?? ids.requestId,
    metadata: event.metadata ?? {},
    ts: new Date().toISOString(),
  };

  if (sink) {
    sink(payload);
    return;
  }

  // PII minimization: sadece güvenli metadata alanları işlenir.
  if (typeof window !== "undefined") {
    // eslint-disable-next-line no-console
    console.info("[telemetry]", payload);
  }
}
