/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: auth + role yönlendirmesi güvenli varsayılanla uygulanır. */

import { NextRequest, NextResponse } from "next/server";

const PUBLIC_PATHS = new Set(["/login", "/", "/api/health"]);
const ROLE_PREFIXES: Record<string, readonly string[]> = {
  admin: ["/analytics", "/audit", "/pricing", "/admin/sla", "/users", "/admin/payments", "/calibration", "/qc", "/api-keys", "/experts", "/pilots"],
  expert: ["/queue", "/review", "/expert/settings", "/expert/sla", "/expert/profile"],
  farmer: ["/fields", "/missions", "/subscriptions", "/results", "/payments"],
  pilot: ["/pilot/missions", "/planner", "/capacity", "/pilot/settings", "/pilot/profile"],
};

function isStaticPath(pathname: string): boolean {
  return pathname.startsWith("/_next") || pathname.startsWith("/icons") || pathname.startsWith("/sounds") || pathname.includes(".");
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (isStaticPath(pathname) || PUBLIC_PATHS.has(pathname)) {
    return NextResponse.next();
  }

  const token = request.cookies.get("ta_token")?.value;
  const role = request.cookies.get("ta_role")?.value;

  if (!token || !role) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  const allowedPrefixes = ROLE_PREFIXES[role] ?? [];
  const isAllowed = allowedPrefixes.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`));

  if (!isAllowed) {
    return NextResponse.redirect(new URL("/forbidden", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/:path*"],
};
