// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export interface MetricItem {
  key: string;
  label: string;
  value: number;
  unit?: string;
}

interface MetricsDashboardProps {
  items: MetricItem[];
}

export function MetricsDashboard({ items }: MetricsDashboardProps) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item) => (
        <Card key={item.key}>
          <CardHeader>
            <CardTitle className="text-sm">{item.label}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-semibold text-slate-900">
              {item.value}
              {item.unit ? <span className="ml-1 text-sm text-slate-500">{item.unit}</span> : null}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
