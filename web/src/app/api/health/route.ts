/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: health endpoint trace-id başlıklarını geri yansıtır. */

import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const corrId = request.headers.get("x-corr-id") ?? "n/a";
  const requestId = request.headers.get("x-request-id") ?? "n/a";

  return NextResponse.json(
    {
      status: "ok",
      service: "tarlaanaliz-web",
      corrId,
      requestId,
      timestamp: new Date().toISOString(),
    },
    {
      status: 200,
      headers: {
        "cache-control": "no-store",
      },
    }
  );
}
