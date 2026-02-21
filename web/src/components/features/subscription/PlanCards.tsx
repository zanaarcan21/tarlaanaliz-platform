// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Button } from '@/components/ui/button';

export interface SubscriptionPlanCard {
  id: string;
  title: string;
  missionLimit: number;
  priceLabel: string;
  recommended?: boolean;
}

interface PlanCardsProps {
  plans: SubscriptionPlanCard[];
  selectedPlanId?: string;
  onSelect: (planId: string) => void;
}

export function PlanCards({ plans, selectedPlanId, onSelect }: PlanCardsProps) {
  return (
    <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3" data-testid="plan-cards">
      {plans.map((plan) => {
        const selected = selectedPlanId === plan.id;
        return (
          <article
            key={plan.id}
            className={`rounded-lg border p-4 ${selected ? 'border-emerald-500 bg-emerald-50' : 'border-slate-200 bg-white'}`}
            data-testid={`plan-card-${plan.id}`}
          >
            <div className="mb-3 flex items-start justify-between gap-3">
              <h3 className="text-base font-semibold text-slate-900">{plan.title}</h3>
              {plan.recommended ? <span className="rounded-full bg-sky-100 px-2 py-1 text-xs font-medium text-sky-700">Önerilen</span> : null}
            </div>
            <p className="text-sm text-slate-600">Görev limiti: {plan.missionLimit}</p>
            <p className="mt-1 text-lg font-semibold text-slate-900">{plan.priceLabel}</p>
            <Button className="mt-3 w-full" variant={selected ? 'secondary' : 'primary'} onClick={() => onSelect(plan.id)}>
              {selected ? 'Seçildi' : 'Planı Seç'}
            </Button>
          </article>
        );
      })}
    </div>
  );
}
