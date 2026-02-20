// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export interface AddFieldPayload {
  name: string;
  areaHectare: number;
  requestId?: string;
  corrId?: string;
}

interface AddFieldModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (payload: AddFieldPayload) => Promise<void> | void;
  requestMeta?: { requestId?: string; corrId?: string };
}

export function AddFieldModal({ open, onClose, onSubmit, requestMeta }: AddFieldModalProps) {
  const [name, setName] = useState('');
  const [areaHectare, setAreaHectare] = useState('');
  const [error, setError] = useState<string | null>(null);

  if (!open) return null;

  const handleSubmit = async () => {
    if (!name.trim()) return setError('Tarla adı zorunludur.');
    const area = Number(areaHectare);
    if (!Number.isFinite(area) || area <= 0) return setError('Alan değeri 0’dan büyük olmalıdır.');
    setError(null);
    await onSubmit({ name: name.trim(), areaHectare: area, ...requestMeta });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" data-request-id={requestMeta?.requestId} data-corr-id={requestMeta?.corrId}>
      <div className="w-full max-w-lg rounded-lg bg-white p-5 shadow-xl">
        <h2 className="text-lg font-semibold text-slate-900">Yeni Tarla Ekle</h2>
        <div className="mt-4 space-y-3">
          <Input placeholder="Tarla adı" value={name} onChange={(e) => setName(e.target.value)} hasError={!!error && !name.trim()} />
          <Input
            type="number"
            inputMode="decimal"
            min={0}
            step="0.01"
            placeholder="Alan (ha)"
            value={areaHectare}
            onChange={(e) => setAreaHectare(e.target.value)}
            hasError={!!error && Number(areaHectare) <= 0}
          />
          {error ? <p className="text-sm text-rose-600">{error}</p> : null}
        </div>
        <div className="mt-4 flex justify-end gap-2">
          <Button variant="secondary" onClick={onClose}>İptal</Button>
          <Button onClick={handleSubmit}>Kaydet</Button>
        </div>
      </div>
    </div>
  );
}
