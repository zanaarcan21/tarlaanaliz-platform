/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

export const tr = {
  common: {
    loading: "Yükleniyor",
    retry: "Tekrar dene",
    empty: "Kayıt bulunamadı",
  },
  expertPortal: {
    queue: {
      title: "İş Kuyruğu",
      queued: "Kuyrukta",
      inReview: "İncelemede",
      completed: "Tamamlanan",
    },
    review: {
      open: "İncelemeyi Aç",
      verdict: "Karar",
    },
  },
} as const;

export type TrDictionary = typeof tr;
