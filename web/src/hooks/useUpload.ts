// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { useCallback, useMemo, useState } from 'react';

interface UploadOptions {
  endpoint: string;
  method?: 'POST' | 'PUT';
}

export function useUpload({ endpoint, method = 'POST' }: UploadOptions) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = useCallback(
    async (file: File, metadata?: Record<string, string>) => {
      setIsUploading(true);
      setError(null);
      try {
        const body = new FormData();
        body.append('file', file);
        Object.entries(metadata ?? {}).forEach(([key, value]) => body.append(key, value));

        const response = await fetch(endpoint, { method, body });
        if (!response.ok) throw new Error('Upload failed');
        return response;
      } catch (uploadError) {
        setError(uploadError instanceof Error ? uploadError.message : 'Upload failed');
        throw uploadError;
      } finally {
        setIsUploading(false);
      }
    },
    [endpoint, method]
  );

  return useMemo(
    () => ({
      upload,
      isUploading,
      error
    }),
    [error, isUploading, upload]
  );
}
