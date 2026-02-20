// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface FieldMapProps {
  provider?: 'leaflet' | 'mapbox' | 'stub';
  fieldName: string;
  coordinates?: Array<[number, number]>;
}

export function FieldMap({ provider = 'stub', fieldName, coordinates = [] }: FieldMapProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{fieldName} Haritası</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">
          Provider: <strong>{provider}</strong> (stub boundary)
          <br />
          Nokta sayısı: {coordinates.length}
        </div>
      </CardContent>
    </Card>
  );
}
