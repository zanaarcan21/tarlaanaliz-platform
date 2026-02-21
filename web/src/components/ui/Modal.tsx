// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import type { ReactNode } from 'react';

import { Button } from './Button';

const cx = (...parts: Array<string | false | null | undefined>) => parts.filter(Boolean).join(' ');

interface ModalProps {
  open: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
  footer?: ReactNode;
  className?: string;
  closeLabel?: string;
}

export function Modal({ open, title, children, onClose, footer, className, closeLabel = 'Kapat' }: ModalProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className={cx('w-full max-w-lg rounded-lg bg-white shadow-xl', className)}>
        <div className="flex items-center justify-between border-b border-slate-100 p-4">
          <h2 id="modal-title" className="text-lg font-semibold text-slate-900">
            {title}
          </h2>
          <Button size="sm" variant="ghost" onClick={onClose} aria-label={closeLabel}>
            ×
          </Button>
        </div>
        <div className="p-4">{children}</div>
        <div className="flex justify-end gap-2 border-t border-slate-100 p-4">{footer}</div>
      </div>
    </div>
  );
}
