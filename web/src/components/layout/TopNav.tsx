// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Button } from '@/components/ui/button';

interface TopNavProps {
  title: string;
  onLogout?: () => void;
  requestMeta?: { requestId?: string; corrId?: string };
}

export function TopNav({ title, onLogout, requestMeta }: TopNavProps) {
  return (
    <header
      className="flex h-14 items-center justify-between border-b border-slate-200 bg-white px-4"
      data-testid="top-nav"
      data-request-id={requestMeta?.requestId}
      data-corr-id={requestMeta?.corrId}
    >
      <h1 className="text-base font-semibold text-slate-900">{title}</h1>
      {onLogout ? (
        <Button data-testid="top-nav-logout" size="sm" variant="secondary" onClick={onLogout}>
          Çıkış
        </Button>
      ) : null}
    </header>
  );
}
