// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import { useState } from 'react';

import { Input } from '@/components/ui/input';

export interface MapLayer {
  id: string;
  name: string;
  visible: boolean;
  opacity: number;
}

interface MapLayerViewerProps {
  layers: MapLayer[];
  onLayersChange?: (layers: MapLayer[]) => void;
}

export function MapLayerViewer({ layers, onLayersChange }: MapLayerViewerProps) {
  const [localLayers, setLocalLayers] = useState(layers);

  const updateLayer = (id: string, patch: Partial<MapLayer>) => {
    const next = localLayers.map((layer) => (layer.id === id ? { ...layer, ...patch } : layer));
    setLocalLayers(next);
    onLayersChange?.(next);
  };

  return (
    <div className="space-y-3 rounded-lg border border-slate-200 p-4">
      {localLayers.map((layer) => (
        <div key={layer.id} className="rounded-md border border-slate-100 p-3">
          <div className="flex items-center justify-between gap-3">
            <label className="flex items-center gap-2 text-sm font-medium text-slate-900">
              <input type="checkbox" checked={layer.visible} onChange={(e) => updateLayer(layer.id, { visible: e.target.checked })} />
              {layer.name}
            </label>
            <Input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={layer.opacity}
              onChange={(e) => updateLayer(layer.id, { opacity: Number(e.target.value) })}
              className="h-2 border-0 p-0"
            />
          </div>
        </div>
      ))}
    </div>
  );
}
