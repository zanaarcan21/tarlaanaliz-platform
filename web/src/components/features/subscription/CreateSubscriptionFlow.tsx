// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface PlanOption {
  id: string;
  name: string;
  missionLimit: number;
}

interface CreateSubscriptionFlowProps {
  plans: PlanOption[];
  onComplete: (planId: string, requestMeta?: { requestId?: string; corrId?: string }) => Promise<void> | void;
  requestMeta?: { requestId?: string; corrId?: string };
}

export function CreateSubscriptionFlow({ plans, onComplete, requestMeta }: CreateSubscriptionFlowProps) {
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(plans[0]?.id ?? null);

  return (
    <Card data-request-id={requestMeta?.requestId} data-corr-id={requestMeta?.corrId}>
      <CardHeader>
        <CardTitle>Abonelik Oluştur</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {plans.map((plan) => (
            <label key={plan.id} className="flex cursor-pointer items-center justify-between rounded-md border border-slate-200 p-3">
              <span>
                <span className="block font-medium text-slate-900">{plan.name}</span>
                <span className="text-sm text-slate-600">Görev limiti: {plan.missionLimit}</span>
              </span>
              <input
                type="radio"
                name="plan"
                checked={selectedPlanId === plan.id}
                onChange={() => setSelectedPlanId(plan.id)}
                aria-label={`${plan.name} planı`}
              />
            </label>
          ))}
        </div>
        <Button className="mt-4" disabled={!selectedPlanId} onClick={() => selectedPlanId && onComplete(selectedPlanId, requestMeta)}>
          Devam Et
        </Button>
      </CardContent>
    </Card>
  );
}
