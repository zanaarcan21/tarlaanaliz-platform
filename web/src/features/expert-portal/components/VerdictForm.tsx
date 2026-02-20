/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Verdict payload contract-first tip ile üretilir. */

import { FormEvent, useState } from "react";

export type VerdictDecision = "approve" | "needs_revision" | "reject";

export interface VerdictPayload {
  readonly reviewId: string;
  readonly decision: VerdictDecision;
  readonly summary: string;
  readonly corrId?: string;
  readonly requestId?: string;
}

export interface VerdictFormProps {
  readonly reviewId: string;
  readonly corrId?: string;
  readonly requestId?: string;
  readonly onSubmitVerdict: (payload: VerdictPayload) => Promise<void>;
}

export function VerdictForm({ reviewId, corrId, requestId, onSubmitVerdict }: VerdictFormProps) {
  const [decision, setDecision] = useState<VerdictDecision>("needs_revision");
  const [summary, setSummary] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!summary.trim()) {
      return;
    }

    setSubmitting(true);
    try {
      await onSubmitVerdict({ reviewId, decision, summary: summary.trim(), corrId, requestId });
      setSummary("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3" data-corr-id={corrId} data-request-id={requestId}>
      <fieldset>
        <legend className="mb-1 font-medium">Karar</legend>
        <label className="mr-3">
          <input
            type="radio"
            name="decision"
            value="approve"
            checked={decision === "approve"}
            onChange={() => setDecision("approve")}
          />
          Onayla
        </label>
        <label className="mr-3">
          <input
            type="radio"
            name="decision"
            value="needs_revision"
            checked={decision === "needs_revision"}
            onChange={() => setDecision("needs_revision")}
          />
          Revizyon
        </label>
        <label>
          <input
            type="radio"
            name="decision"
            value="reject"
            checked={decision === "reject"}
            onChange={() => setDecision("reject")}
          />
          Reddet
        </label>
      </fieldset>

      <div>
        <label htmlFor="verdict-summary" className="mb-1 block font-medium">
          Expert Notu
        </label>
        <textarea
          id="verdict-summary"
          name="summary"
          value={summary}
          onChange={(event) => setSummary(event.target.value)}
          rows={4}
          required
          className="w-full rounded border p-2"
        />
      </div>

      <button type="submit" disabled={submitting} className="rounded border px-3 py-2 disabled:opacity-70">
        {submitting ? "Gönderiliyor..." : "Kararı Gönder"}
      </button>
    </form>
  );
}
