// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import type { ReactNode } from 'react';

import { SideNav } from './SideNav';
import { TopNav } from './TopNav';

interface AppShellProps {
  title: string;
  children: ReactNode;
  navItems: Array<{ href: string; label: string; testId: string }>;
  activeHref?: string;
  onLogout?: () => void;
  requestMeta?: { requestId?: string; corrId?: string };
}

export function AppShell({ title, children, navItems, activeHref, onLogout, requestMeta }: AppShellProps) {
  return (
    <div className="min-h-screen bg-slate-50" data-testid="app-shell">
      <TopNav title={title} onLogout={onLogout} requestMeta={requestMeta} />
      <div className="flex">
        <SideNav items={navItems} activeHref={activeHref} />
        <main className="flex-1 p-4" data-testid="app-shell-content">
          {children}
        </main>
      </div>
    </div>
  );
}
