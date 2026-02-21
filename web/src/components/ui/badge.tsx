// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import type { HTMLAttributes } from 'react';

type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info';

const badgeVariantClass: Record<BadgeVariant, string> = {
  default: 'bg-slate-100 text-slate-800',
  success: 'bg-emerald-100 text-emerald-800',
  warning: 'bg-amber-100 text-amber-800',
  danger: 'bg-rose-100 text-rose-800',
  info: 'bg-sky-100 text-sky-800'
};

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

export function Badge({ className = '', variant = 'default', ...props }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold ${badgeVariantClass[variant]} ${className}`.trim()}
      {...props}
    />
  );
}
