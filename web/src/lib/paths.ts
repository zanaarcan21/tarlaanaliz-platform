/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

export const paths = {
  home: "/",
  auth: {
    login: "/auth/login",
    logout: "/auth/logout",
  },
  expertPortal: {
    dashboard: "/expert-portal",
    queue: "/expert-portal/queue",
    review: (reviewId: string) => `/expert-portal/reviews/${encodeURIComponent(reviewId)}`,
  },
  results: {
    index: "/results",
    detail: (resultId: string) => `/results/${encodeURIComponent(resultId)}`,
  },
} as const;
