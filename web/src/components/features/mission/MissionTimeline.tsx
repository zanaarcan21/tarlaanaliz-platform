// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Badge } from '@/components/ui/badge';

export interface TimelineStep {
  id: string;
  title: string;
  timestamp: string;
  state: 'done' | 'current' | 'pending' | 'error';
  requestId?: string;
  corrId?: string;
}

interface MissionTimelineProps {
  steps: TimelineStep[];
}

const stateVariant = {
  done: 'success',
  current: 'info',
  pending: 'default',
  error: 'danger'
} as const;

export function MissionTimeline({ steps }: MissionTimelineProps) {
  return (
    <ol className="space-y-3" aria-label="Mission timeline">
      {steps.map((step) => (
        <li key={step.id} className="rounded-md border border-slate-200 p-3" data-request-id={step.requestId} data-corr-id={step.corrId}>
          <div className="flex items-center justify-between">
            <p className="font-medium text-slate-900">{step.title}</p>
            <Badge variant={stateVariant[step.state]}>{step.state}</Badge>
          </div>
          <p className="mt-1 text-xs text-slate-500">{new Date(step.timestamp).toLocaleString('tr-TR')}</p>
        </li>
      ))}
    </ol>
  );
}
