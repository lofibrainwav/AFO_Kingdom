import type { NextConfig } from "next";

// Environment-aware Soul Engine URL
// - Local dev: Use localhost (Next.js process runs on host machine)
// - Docker build: Use container DNS (SOUL_ENGINE_URL env var or Docker name)
const soulEngineUrl = process.env.BACKEND_BASE_URL || "http://127.0.0.1:8010";

const nextConfig: NextConfig = {
  /* config options here */
  output: "standalone",
  
  // 성능 최적화 설정
  experimental: {
    // Note: Turbopack은 dev 명령어에 --turbo 플래그가 없으면 자동으로 webpack 사용
    // Next.js 16에서는 experimental.turbo 속성이 없음
    optimizePackageImports: [
      "framer-motion",
      "lucide-react",
      "recharts",
      "@radix-ui/react-avatar",
      "@radix-ui/react-slot",
    ],
  },
  
  // 이미지 최적화
  images: {
    formats: ["image/avif", "image/webp"],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${soulEngineUrl}/:path*`, // Generic Proxy to Backend
      },
    ];
  },
};

export default nextConfig;
