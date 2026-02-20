// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import { useMemo, useState } from 'react';

import { Button } from '@/components/ui/button';

const MAX_FILE_SIZE_MB = 10;
const ACCEPTED_TYPES = ['image/png', 'image/jpeg', 'application/pdf'];

export interface UploadMeta {
  requestId?: string;
  corrId?: string;
}

interface PaymentUploadProps {
  onUpload: (file: File, meta?: UploadMeta) => Promise<void> | void;
  requestMeta?: UploadMeta;
}

export function PaymentUpload({ onUpload, requestMeta }: PaymentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const acceptedText = useMemo(() => ACCEPTED_TYPES.join(', '), []);

  const validate = (candidate: File) => {
    if (!ACCEPTED_TYPES.includes(candidate.type)) return 'Desteklenmeyen dosya tipi.';
    if (candidate.size > MAX_FILE_SIZE_MB * 1024 * 1024) return `Dosya boyutu ${MAX_FILE_SIZE_MB}MB üstünde olamaz.`;
    return null;
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selected = event.target.files?.[0];
    if (!selected) return;
    const nextError = validate(selected);
    setError(nextError);
    setFile(nextError ? null : selected);
  };

  const handleUpload = async () => {
    if (!file) return;
    await onUpload(file, requestMeta);
  };

  return (
    <section className="space-y-3 rounded-lg border border-slate-200 p-4" data-request-id={requestMeta?.requestId} data-corr-id={requestMeta?.corrId}>
      <h3 className="text-base font-semibold text-slate-900">Dekont Yükle</h3>
      <p className="text-sm text-slate-600">PII içermeyen dekont dosyasını yükleyin.</p>
      <input type="file" accept={acceptedText} onChange={handleFileChange} className="block w-full text-sm" aria-describedby="payment-upload-hint" />
      <p id="payment-upload-hint" className="text-xs text-slate-500">İzinli tipler: PNG, JPEG, PDF • Maksimum {MAX_FILE_SIZE_MB}MB</p>
      {error ? <p className="text-sm text-rose-600">{error}</p> : null}
      <Button onClick={handleUpload} disabled={!file || !!error}>Yüklemeyi Başlat</Button>
    </section>
  );
}
