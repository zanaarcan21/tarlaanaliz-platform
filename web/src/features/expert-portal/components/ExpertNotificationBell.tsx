/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: YZ/iş akışı bildirimleri platformda izlenebilir metadata ile taşınır. */

import { useEffect, useMemo, useRef } from "react";

export interface ExpertNotificationBellProps {
  readonly unreadCount: number;
  readonly onOpen: () => void;
  readonly disabled?: boolean;
  readonly corrId?: string;
  readonly requestId?: string;
  readonly notificationSoundPath?: string;
}

export function ExpertNotificationBell({
  unreadCount,
  onOpen,
  disabled = false,
  corrId,
  requestId,
  notificationSoundPath = "/sounds/notification.mp3",
}: ExpertNotificationBellProps) {
  const previousUnreadCount = useRef(unreadCount);
  const audio = useMemo(() => new Audio(notificationSoundPath), [notificationSoundPath]);

  useEffect(() => {
    if (unreadCount > previousUnreadCount.current) {
      audio.currentTime = 0;
      void audio.play().catch(() => {
        // Browser autoplay policy can block playback.
      });
    }

    previousUnreadCount.current = unreadCount;

    return () => {
      audio.pause();
    };
  }, [audio, unreadCount]);

  return (
    <button
      type="button"
      onClick={onOpen}
      disabled={disabled}
      aria-label={`Bildirimler, ${unreadCount} okunmamış`}
      aria-live="polite"
      data-corr-id={corrId}
      data-request-id={requestId}
      className="relative inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
    >
      <span aria-hidden="true">🔔</span>
      {unreadCount > 0 ? (
        <span className="absolute -right-1 -top-1 min-w-5 rounded-full bg-red-600 px-1 text-center text-xs font-semibold text-white">
          {unreadCount > 99 ? "99+" : unreadCount}
        </span>
      ) : null}
    </button>
  );
}
