// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  testId?: string;
}

export function EmptyState({ title, description, actionLabel, onAction, testId = 'empty-state' }: EmptyStateProps) {
  return (
    <section className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center" data-testid={testId}>
      <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
      {actionLabel && onAction ? (
        <Button className="mt-4" variant="secondary" onClick={onAction} data-testid={`${testId}-action`}>
          {actionLabel}
        </Button>
      ) : null}
    </section>
  );
}
