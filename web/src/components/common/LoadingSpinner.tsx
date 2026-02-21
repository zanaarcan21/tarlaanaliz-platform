// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import type { HTMLAttributes } from 'react';

interface LoadingSpinnerProps extends HTMLAttributes<HTMLDivElement> {
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

const sizeClass = { sm: 'h-4 w-4 border-2', md: 'h-6 w-6 border-2', lg: 'h-10 w-10 border-[3px]' };

export function LoadingSpinner({ label = 'Yükleniyor', size = 'md', className = '', ...props }: LoadingSpinnerProps) {
  return (
    <div role="status" aria-label={label} className={`inline-flex items-center gap-2 ${className}`.trim()} {...props}>
      <span className={`inline-block animate-spin rounded-full border-emerald-600 border-t-transparent ${sizeClass[size]}`} />
      <span className="text-sm text-slate-600">{label}</span>
    </div>
  );
}
