/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: role/auth guard akışında izlenebilir yönlendirme. */

import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import type { ReactNode } from "react";

interface AdminLayoutProps {
  readonly children: ReactNode;
}

const navItems = [
  { href: "/analytics", label: "Analytics" },
  { href: "/audit", label: "Audit" },
  { href: "/pricing", label: "Pricing" },
  { href: "/sla", label: "SLA" },
  { href: "/users", label: "Users" },
] as const;

export default function AdminLayout({ children }: AdminLayoutProps) {
  const cookieStore = cookies();
  const token = cookieStore.get("ta_token")?.value;
  const role = cookieStore.get("ta_role")?.value;

  if (!token) {
    redirect("/login");
  }

  if (role !== "admin") {
    redirect("/forbidden");
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 md:grid-cols-[240px_1fr]">
        <aside className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-3 text-sm font-semibold text-slate-600">Admin</h2>
          <nav aria-label="Admin navigation" className="space-y-2">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href} className="block rounded px-2 py-1 text-sm hover:bg-slate-100">
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>
        <main>{children}</main>
      </div>
    </div>
  );
}
