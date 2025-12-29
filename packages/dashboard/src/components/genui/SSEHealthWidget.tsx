/**
 * SSE Health Widget - Real-time SSE Connection Monitoring
 *
 * Shows SSE connection health with 3 key metrics:
 * - Current open connections
 * - Recent reconnect count
 * - Last event age
 *
 * Status: 🟢 OK / 🟡 STALE / 🔴 DOWN
 */
'use client';

import { useState, useEffect, useRef } from 'react';
import { Activity, Wifi, WifiOff, AlertTriangle } from 'lucide-react';
import { createEventSource, SSE_ENDPOINTS } from '@/lib/sse';

type SSEHealthStatus = 'ok' | 'stale' | 'down';

interface SSEMetrics {
  openConnections: number;
  reconnectCount: number;
  lastEventAgeSeconds: number;
  status: SSEHealthStatus;
}

const SSEHealthWidget = () => {
  const [metrics, setMetrics] = useState<SSEMetrics>({
    openConnections: 0,
    reconnectCount: 0,
    lastEventAgeSeconds: 0,
    status: 'ok'
  });

  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const lastEventRef = useRef<number>(Date.now());
  const reconnectCountRef = useRef<number>(0);

  // Update last event timestamp
  const updateLastEvent = () => {
    lastEventRef.current = Date.now();
  };

  // Calculate metrics and status
  const updateMetrics = () => {
    const now = Date.now();
    const ageSeconds = Math.floor((now - lastEventRef.current) / 1000);

    let status: SSEHealthStatus = 'ok';
    if (ageSeconds > 30) status = 'stale';
    if (ageSeconds > 60 || !isConnected) status = 'down';

    setMetrics({
      openConnections: isConnected ? 1 : 0,
      reconnectCount: reconnectCountRef.current,
      lastEventAgeSeconds: ageSeconds,
      status
    });
  };

  useEffect(() => {
    // Prevent duplicate connections in React dev StrictMode
    if (eventSourceRef.current) return;

    const eventSource = createEventSource(SSE_ENDPOINTS.LOGS);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      console.log('[SSEHealth] Connected');
      setIsConnected(true);
      reconnectCountRef.current = 0;
      updateLastEvent();
    };

    eventSource.onmessage = () => {
      updateLastEvent();
    };

    eventSource.onerror = () => {
      console.log('[SSEHealth] Connection error');
      setIsConnected(false);
      eventSource.close();
      eventSourceRef.current = null;

      // Simple reconnect with backoff
      setTimeout(() => {
        reconnectCountRef.current += 1;
      }, 2000);
    };

    // Update metrics every 5 seconds
    const metricsInterval = setInterval(updateMetrics, 5000);

    return () => {
      console.log('[SSEHealth] Cleanup');
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
      clearInterval(metricsInterval);
    };
  }, []);

  // Update metrics on state changes
  useEffect(() => {
    updateMetrics();
  }, [isConnected]);

  const getStatusIcon = () => {
    switch (metrics.status) {
      case 'ok':
        return <Wifi className="w-5 h-5 text-green-500" />;
      case 'stale':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'down':
        return <WifiOff className="w-5 h-5 text-red-500" />;
    }
  };

  const getStatusText = () => {
    switch (metrics.status) {
      case 'ok':
        return 'SSE Healthy';
      case 'stale':
        return 'SSE Stale';
      case 'down':
        return 'SSE Down';
    }
  };

  const getStatusColor = () => {
    switch (metrics.status) {
      case 'ok':
        return 'bg-green-50 border-green-200';
      case 'stale':
        return 'bg-yellow-50 border-yellow-200';
      case 'down':
        return 'bg-red-50 border-red-200';
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getStatusColor()}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-gray-600" />
          <span className="text-sm font-medium text-gray-700">SSE Health</span>
        </div>
        <div className="flex items-center gap-2">
          {getStatusIcon()}
          <span className="text-xs font-medium">{getStatusText()}</span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4 text-xs">
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-800">
            {metrics.openConnections}
          </div>
          <div className="text-gray-600">Connections</div>
        </div>

        <div className="text-center">
          <div className="text-lg font-semibold text-gray-800">
            {metrics.reconnectCount}
          </div>
          <div className="text-gray-600">Reconnects</div>
        </div>

        <div className="text-center">
          <div className="text-lg font-semibold text-gray-800">
            {metrics.lastEventAgeSeconds}s
          </div>
          <div className="text-gray-600">Last Event</div>
        </div>
      </div>
    </div>
  );
};

export default SSEHealthWidget;
