// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Button } from '@/components/ui/button';

export interface ResultLayer {
  id: string;
  title: string;
  selected: boolean;
}

interface LayerListProps {
  layers: ResultLayer[];
  onToggle: (id: string) => void;
}

export function LayerList({ layers, onToggle }: LayerListProps) {
  return (
    <ul className="space-y-2">
      {layers.map((layer) => (
        <li key={layer.id} className="flex items-center justify-between rounded-md border border-slate-200 p-3">
          <span className="text-sm font-medium text-slate-900">{layer.title}</span>
          <Button variant="secondary" size="sm" onClick={() => onToggle(layer.id)}>
            {layer.selected ? 'Gizle' : 'Göster'}
          </Button>
        </li>
      ))}
    </ul>
  );
}
