// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import Link from 'next/link';

interface SideNavItem {
  href: string;
  label: string;
  testId: string;
}

interface SideNavProps {
  items: SideNavItem[];
  activeHref?: string;
}

export function SideNav({ items, activeHref }: SideNavProps) {
  return (
    <aside className="w-64 border-r border-slate-200 bg-white p-3" data-testid="side-nav">
      <nav>
        <ul className="space-y-1">
          {items.map((item) => {
            const isActive = item.href === activeHref;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  data-testid={item.testId}
                  className={`block rounded-md px-3 py-2 text-sm ${
                    isActive ? 'bg-emerald-50 font-medium text-emerald-800' : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
