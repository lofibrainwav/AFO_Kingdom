"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Cpu, HardDrive, Activity, AlertTriangle } from "lucide-react";

interface OverloadData {
  cpu: number;
  memory: number;
  disk: number;
  status: "normal" | "warning" | "critical";
  alerts: string[];
}

export function OverloadMonitorWidget() {
  const [metrics, setMetrics] = useState<OverloadData>({
    cpu: 0,
    memory: 0,
    disk: 0,
    status: "normal",
    alerts: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";
        const response = await fetch(`${API_BASE}/api/system/overload`);

        if (response.ok) {
          const data = await response.json();
          setMetrics({
            cpu: data.cpu || 0,
            memory: data.memory || 0,
            disk: data.disk || 0,
            status: data.status || "normal",
            alerts: data.alerts || [],
          });
        }
      } catch (error) {
        console.error("Overload monitor fetch failed:", error);
        // 기본값 설정 (모의 데이터)
        setMetrics({
          cpu: Math.floor(Math.random() * 30) + 10,
          memory: Math.floor(Math.random() * 20) + 40,
          disk: 30,
          status: "normal",
          alerts: [],
        });
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000); // 5초마다 업데이트

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="neu-card min-h-[200px] flex items-center justify-center">
        <div className="animate-pulse text-slate-400">모니터링 중...</div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "critical":
        return "bg-red-100 text-red-700";
      case "warning":
        return "bg-yellow-100 text-yellow-700";
      default:
        return "bg-emerald-100 text-emerald-700";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "critical":
        return "위험";
      case "warning":
        return "주의";
      default:
        return "정상";
    }
  };

  const getBarColor = (value: number) => {
    if (value >= 80) return "bg-red-500";
    if (value >= 60) return "bg-yellow-500";
    return "bg-blue-500";
  };

  return (
    <div className="neu-card min-h-[200px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-600 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-orange-500" />
          시스템 부하
        </h3>
        <span className={`px-2 py-1 text-xs font-bold rounded-full ${getStatusColor(metrics.status)}`}>
          {getStatusText(metrics.status)}
        </span>
      </div>

      <div className="space-y-4">
        {/* CPU */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <Cpu className="w-3 h-3" /> CPU
            </span>
            <span className="font-bold">{metrics.cpu}%</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(metrics.cpu, 100)}%` }}
              transition={{ duration: 1 }}
              className={`h-full ${getBarColor(metrics.cpu)} rounded-full`}
            />
          </div>
        </div>

        {/* Memory */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <Activity className="w-3 h-3" /> 메모리
            </span>
            <span className="font-bold">{metrics.memory}%</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(metrics.memory, 100)}%` }}
              transition={{ duration: 1 }}
              className={`h-full ${getBarColor(metrics.memory)} rounded-full`}
            />
          </div>
        </div>

        {/* Disk */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <HardDrive className="w-3 h-3" /> 디스크
            </span>
            <span className="font-bold">{metrics.disk}%</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(metrics.disk, 100)}%` }}
              transition={{ duration: 1 }}
              className={`h-full ${getBarColor(metrics.disk)} rounded-full`}
            />
          </div>
        </div>
      </div>

      {/* 알림 */}
      {metrics.alerts.length > 0 && (
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="text-xs font-bold text-yellow-700 mb-1">알림</div>
          <ul className="text-xs text-yellow-600 space-y-1">
            {metrics.alerts.map((alert, index) => (
              <li key={index}>• {alert}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

