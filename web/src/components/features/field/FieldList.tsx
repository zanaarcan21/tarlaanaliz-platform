// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export interface FieldSummary {
  id: string;
  name: string;
  areaHectare: number;
}

interface FieldListProps {
  fields: FieldSummary[];
  onSelectField?: (fieldId: string) => void;
}

export function FieldList({ fields, onSelectField }: FieldListProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Tarlalar</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {fields.map((field) => (
            <li key={field.id} className="flex items-center justify-between rounded-md border border-slate-200 p-3">
              <div>
                <p className="font-medium text-slate-900">{field.name}</p>
                <p className="text-sm text-slate-600">{field.areaHectare.toFixed(2)} ha</p>
              </div>
              {onSelectField ? (
                <Button variant="secondary" size="sm" onClick={() => onSelectField(field.id)}>
                  Gör
                </Button>
              ) : null}
            </li>
          ))}
          {fields.length === 0 ? <li className="text-sm text-slate-500">Tarla kaydı bulunamadı.</li> : null}
        </ul>
      </CardContent>
    </Card>
  );
}
