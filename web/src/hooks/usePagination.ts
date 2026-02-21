// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { useMemo, useState } from 'react';

interface PaginationOptions {
  initialPage?: number;
  pageSize?: number;
}

export function usePagination<T>(items: T[], options?: PaginationOptions) {
  const pageSize = options?.pageSize ?? 10;
  const [page, setPage] = useState(options?.initialPage ?? 1);

  const totalPages = Math.max(1, Math.ceil(items.length / pageSize));
  const safePage = Math.min(page, totalPages);

  const pageItems = useMemo(() => {
    const start = (safePage - 1) * pageSize;
    return items.slice(start, start + pageSize);
  }, [items, pageSize, safePage]);

  return {
    page: safePage,
    pageSize,
    totalPages,
    setPage,
    nextPage: () => setPage((p) => Math.min(totalPages, p + 1)),
    prevPage: () => setPage((p) => Math.max(1, p - 1)),
    pageItems
  };
}
