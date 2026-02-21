// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Badge } from '@/components/ui/badge';

export type PaymentStatus = 'pending' | 'receipt_uploaded' | 'manual_review' | 'approved' | 'rejected';

const badgeVariantByStatus = {
  pending: 'warning',
  receipt_uploaded: 'info',
  manual_review: 'warning',
  approved: 'success',
  rejected: 'danger'
} as const;

export function PaymentStatusBadge({ status }: { status: PaymentStatus }) {
  // KR-033: paid/approved yalnızca dekont + manuel onay + audit akışı sonunda olur.
  return <Badge variant={badgeVariantByStatus[status]}>{status}</Badge>;
}
