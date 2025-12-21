import type { NextConfig } from "next";

// Get backend URL from environment variable with fallback
const soulEngineUrl = process.env.SOUL_ENGINE_URL || 'http://127.0.0.1:8010';

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/api/proxy/:path*',
        destination: `${soulEngineUrl}/:path*`, // Proxy to Soul Engine
      },
    ];
  },
};

export default nextConfig;
