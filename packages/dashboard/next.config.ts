import type { NextConfig } from "next";

// Get backend URL from environment variable with fallback
const soulEngineUrl = process.env.SOUL_ENGINE_URL || "http://127.0.0.1:8010";

const nextConfig: NextConfig = {
  /* config options here */
  output: "standalone",
  
  // 성능 최적화 설정
  experimental: {
    optimizePackageImports: [
      "framer-motion",
      "lucide-react",
      "recharts",
      "@radix-ui/react-avatar",
      "@radix-ui/react-slot",
    ],
  },
  
  // 번들 최적화
  webpack: (config, { isServer }) => {
    // Tree-shaking 최적화
    config.optimization = {
      ...config.optimization,
      usedExports: true,
      sideEffects: false,
    };
    
    return config;
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
        source: "/api/proxy/:path*",
        destination: `${soulEngineUrl}/:path*`, // Proxy to Soul Engine
      },
      // Strangler Fig Pattern: Legacy HTML dashboard (port 8000) proxy
      // This allows gradual migration from kingdom_dashboard.html to Next.js
      {
        source: "/docs/legacy/:path*",
        destination: "http://localhost:8000/:path*",
      },
    ];
  },
};

export default nextConfig;
