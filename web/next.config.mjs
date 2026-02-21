/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-071: Response header seviyesinde corr/request izlerinin taşınmasına izin verilir. */

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          {
            key: "x-app-name",
            value: "tarlaanaliz-web",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
