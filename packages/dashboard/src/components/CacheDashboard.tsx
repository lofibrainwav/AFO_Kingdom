"use client";

import { useEffect, useState } from 'react';

interface CacheMetrics {
  total_requests: number;
  cache_hits: number;
  cache_misses: number;
  l1_hits: number;
  l2_hits: number;
  predictive_hits: number;
  hit_rate: number;
  avg_response_time_ms: number;
  uptime_seconds: number;
}

export default function CacheDashboard() {
  const [metrics, setMetrics] = useState<CacheMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/cache/metrics');
        if (response.ok) {
          const data = await response.json();
          setMetrics(data);
        }
      } catch (error) {
        console.error('Failed to fetch cache metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg">
        <div className="animate-pulse">
          <div className="h-6 bg-blue-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-blue-200 rounded w-1/2"></div>
            <div className="h-4 bg-blue-200 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="p-6 bg-red-50 rounded-lg">
        <p className="text-red-600">Failed to load cache metrics</p>
      </div>
    );
  }

  const hitRatePercentage = (metrics.hit_rate * 100).toFixed(1);
  const uptimeMinutes = Math.floor(metrics.uptime_seconds / 60);

  return (
    <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-blue-900 mb-6 flex items-center">
        <span className="mr-2">⚡</span>
        Phase 6B Cache Revolution Dashboard
      </h2>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-green-600">{hitRatePercentage}%</div>
          <div className="text-sm text-gray-600">Cache Hit Rate</div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-blue-600">{metrics.total_requests}</div>
          <div className="text-sm text-gray-600">Total Requests</div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-purple-600">{metrics.avg_response_time_ms.toFixed(1)}ms</div>
          <div className="text-sm text-gray-600">Avg Response Time</div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-orange-600">{uptimeMinutes}m</div>
          <div className="text-sm text-gray-600">Uptime</div>
        </div>
      </div>

      {/* Detailed Metrics */}
      <div className="bg-white rounded-lg p-6 shadow">
        <h3 className="text-lg font-semibold mb-4">Cache Layer Performance</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* L1 Memory Cache */}
          <div className="text-center">
            <div className="text-3xl mb-2">🧠</div>
            <div className="text-xl font-bold text-green-600">{metrics.l1_hits}</div>
            <div className="text-sm text-gray-600">L1 Memory Hits</div>
            <div className="text-xs text-gray-400 mt-1">Fastest (1ms)</div>
          </div>

          {/* L2 Redis Cache */}
          <div className="text-center">
            <div className="text-3xl mb-2">🔴</div>
            <div className="text-xl font-bold text-blue-600">{metrics.l2_hits}</div>
            <div className="text-sm text-gray-600">L2 Redis Hits</div>
            <div className="text-xs text-gray-400 mt-1">Shared (50ms)</div>
          </div>

          {/* Predictive Cache */}
          <div className="text-center">
            <div className="text-3xl mb-2">🔮</div>
            <div className="text-xl font-bold text-purple-600">{metrics.predictive_hits}</div>
            <div className="text-sm text-gray-600">Predictive Hits</div>
            <div className="text-xs text-gray-400 mt-1">AI-Powered</div>
          </div>
        </div>

        {/* Performance Bars */}
        <div className="mt-6">
          <h4 className="text-md font-semibold mb-3">Cache Distribution</h4>
          <div className="space-y-2">
            <div className="flex items-center">
              <span className="w-20 text-sm">Hits</span>
              <div className="flex-1 bg-gray-200 rounded-full h-4 ml-2">
                <div
                  className="bg-green-500 h-4 rounded-full"
                  style={{ width: `${(metrics.cache_hits / Math.max(metrics.total_requests, 1)) * 100}%` }}
                ></div>
              </div>
              <span className="ml-2 text-sm font-semibold">{metrics.cache_hits}</span>
            </div>

            <div className="flex items-center">
              <span className="w-20 text-sm">Misses</span>
              <div className="flex-1 bg-gray-200 rounded-full h-4 ml-2">
                <div
                  className="bg-red-500 h-4 rounded-full"
                  style={{ width: `${(metrics.cache_misses / Math.max(metrics.total_requests, 1)) * 100}%` }}
                ></div>
              </div>
              <span className="ml-2 text-sm font-semibold">{metrics.cache_misses}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Phase 6C Goals Progress */}
      <div className="mt-6 bg-white rounded-lg p-6 shadow">
        <h3 className="text-lg font-semibold mb-4">Phase 6C Goals Progress</h3>
        <div className="space-y-3">
          <div className="flex items-center">
            <span className="w-32 text-sm">LLM Cache Hit</span>
            <div className="flex-1 bg-gray-200 rounded-full h-3 ml-2">
              <div
                className="bg-blue-500 h-3 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(parseFloat(hitRatePercentage), 95)}%` }}
              ></div>
            </div>
            <span className="ml-2 text-sm">{hitRatePercentage}% / 95%</span>
          </div>

          <div className="flex items-center">
            <span className="w-32 text-sm">Response Time</span>
            <div className="flex-1 bg-gray-200 rounded-full h-3 ml-2">
              <div
                className="bg-green-500 h-3 rounded-full transition-all duration-300"
                style={{ width: `${Math.max(0, 100 - (metrics.avg_response_time_ms / 50) * 100)}%` }}
              ></div>
            </div>
            <span className="ml-2 text-sm">{metrics.avg_response_time_ms.toFixed(1)}ms / 50ms</span>
          </div>
        </div>
      </div>
    </div>
  );
}
