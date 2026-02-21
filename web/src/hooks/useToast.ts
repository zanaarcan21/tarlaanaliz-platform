// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { useToast as useToastProvider } from '@/components/common/ToastProvider';

interface ToastMeta {
  requestId?: string;
  corrId?: string;
}

export function useToast() {
  const { showToast } = useToastProvider();

  return {
    success: (message: string, meta?: ToastMeta) => showToast({ type: 'success', message, ...meta }),
    error: (message: string, meta?: ToastMeta) => showToast({ type: 'error', message, ...meta }),
    info: (message: string, meta?: ToastMeta) => showToast({ type: 'info', message, ...meta })
  };
}
