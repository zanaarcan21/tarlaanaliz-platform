/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: global metadata/trace yapısı genişlemeye açık tutulur. */

import type { Metadata } from "next";
import type { ReactNode } from "react";

import "../styles/globals.css";

export const metadata: Metadata = {
  title: "TarlaAnaliz Platform",
  description: "Role-based workflows for admin, expert, farmer and pilot users.",
};

interface RootLayoutProps {
  readonly children: ReactNode;
}

function AppProviders({ children }: RootLayoutProps) {
  // Theme/Auth/Query provider zinciri için genişleme noktası.
  return <>{children}</>;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="tr">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
