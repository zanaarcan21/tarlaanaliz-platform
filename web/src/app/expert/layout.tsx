/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
import type { ReactNode } from "react";

interface PlaceholderLayoutProps {
  readonly children: ReactNode;
}

export default function PlaceholderLayout({ children }: PlaceholderLayoutProps) {
  return <>{children}</>;
}
