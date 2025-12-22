import type { NextConfig } from "next";

// Get backend URL from environment variable with fallback
const soulEngineUrl = process.env.SOUL_ENGINE_URL || "http://127.0.0.1:8010";

const nextConfig: NextConfig = {
  /* config options here */
  output: "standalone",
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
