// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import { forwardRef } from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  hasError?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { className = '', hasError = false, ...props },
  ref
) {
  return (
    <input
      ref={ref}
      className={`h-10 w-full rounded-md border px-3 text-sm shadow-sm outline-none transition placeholder:text-slate-400 focus-visible:ring-2 ${
        hasError
          ? 'border-rose-500 focus-visible:ring-rose-400'
          : 'border-slate-300 focus-visible:ring-emerald-500'
      } ${className}`.trim()}
      {...props}
    />
  );
});
