// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { useEffect, useMemo, useState } from 'react';

export interface FeatureFlags {
  newMissionPlanner: boolean;
  paymentManualReviewUI: boolean;
  resultGalleryV2: boolean;
}

const localDefaults: FeatureFlags = {
  newMissionPlanner: false,
  paymentManualReviewUI: true,
  resultGalleryV2: false
};

export function useFeatureFlags() {
  const [flags, setFlags] = useState<FeatureFlags>(localDefaults);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;

    const load = async () => {
      setLoading(true);
      try {
        const response = await fetch('/api/feature-flags');
        if (!response.ok) return;
        const serverFlags = (await response.json()) as Partial<FeatureFlags>;
        if (active) setFlags((prev) => ({ ...prev, ...serverFlags }));
      } finally {
        if (active) setLoading(false);
      }
    };

    void load();

    return () => {
      active = false;
    };
  }, []);

  return useMemo(
    () => ({
      flags,
      loading,
      isEnabled: (flag: keyof FeatureFlags) => Boolean(flags[flag])
    }),
    [flags, loading]
  );
}
