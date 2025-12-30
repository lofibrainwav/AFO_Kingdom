import type { NextConfig } from "next";

// Environment-aware Soul Engine URL
// - Local dev: Use localhost (Next.js process runs on host machine)
// - Docker build: Use container DNS (SOUL_ENGINE_URL env var or Docker name)
const soulEngineUrl = process.env.SOUL_ENGINE_URL || "http://localhost:8010";

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
  
  // Turbopack 설정 (Next.js 16 기본 활성화, webpack과 충돌 방지)
  // turbopack: {}, // Removed due to workspace root ambiguity in Turbopack
  
  // 번들 최적화
  /* 
  webpack: (config, { isServer }) => {
    // Tree-shaking 최적화 (Next.js 16 기본 최적화와 충돌 가능성으로 주석 처리)
    config.optimization = {
      ...config.optimization,
      usedExports: true,
      sideEffects: false,
    };
    
    return config;
  },
  */
  
  // 이미지 최적화
  images: {
    formats: ["image/avif", "image/webp"],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  
  async rewrites() {
    return [
      // Health check proxy for smoke tests
      {
        source: "/api/health",
        destination: `${soulEngineUrl}/api/health`,
      },
      // SSE Stream Proxy - SSOT: /api/logs/stream
      {
        source: "/api/logs/stream",
        destination: `${soulEngineUrl}/api/logs/stream`,  // SSOT canonical path
      },
      // Legacy Path 1 (Internal Forwarding)
      {
        source: "/api/stream/logs",
        destination: `${soulEngineUrl}/api/logs/stream`,
      },
      // Legacy Path 2 (Internal Forwarding)
      {
        source: "/api/system/logs/stream",
        destination: `${soulEngineUrl}/api/logs/stream`,
      },
      // Generic proxy (after specific routes)
      {
        source: "/api/proxy/:path*",
        destination: `${soulEngineUrl}/:path*`, // Proxy to Soul Engine
      },
      // Legacy HTML은 public/legacy/로 직접 서빙 (8000 포트 불필요)
      // Next.js는 public/legacy/*를 자동으로 /legacy/*로 서빙합니다.
    ];
  },
};

export default nextConfig;
