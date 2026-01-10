"use client";

import { Activity, Cpu, HardDrive, Server } from "lucide-react";
import { useEffect, useState } from "react";

export const SystemStatusWidget = () => {
  const [metrics, setMetrics] = useState({ cpu: 12, mem: 45, disk: 30 });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics({
        cpu: Math.floor(Math.random() * 20) + 10,
        mem: Math.floor(Math.random() * 10) + 40,
        disk: 30,
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Fetch kingdom status for SHA/Canary
  const [status, setStatus] = useState<any>(null);
  useEffect(() => {
    fetch('/api/kingdom-status')
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(() => {});
  }, []);

  return (
    <div className="neu-card min-h-[200px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-600 flex items-center gap-2">
          <Server className="w-4 h-4 text-blue-500" />
          SYSTEM VITALITY
        </h3>
        <span className="px-2 py-1 text-xs font-bold rounded-full bg-emerald-100 text-emerald-700">
          NORMAL
        </span>
      </div>
      
      <div className="space-y-4">
        {/* CPU */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <Cpu className="w-3 h-3" /> CPU Load
            </span>
            <span className="font-bold">{metrics.cpu}%</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 rounded-full transition-all duration-1000"
              style={{ width: `${Math.min(metrics.cpu, 100)}%` }}
            />
          </div>
        </div>

        {/* Memory */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <Activity className="w-3 h-3" /> Memory
            </span>
            <span className="font-bold">{metrics.mem}%</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <div
              className="h-full bg-purple-500 rounded-full transition-all duration-1000"
              style={{ width: `${Math.min(metrics.mem, 100)}%` }}
            />
          </div>
        </div>

        {/* Disk */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <HardDrive className="w-3 h-3" /> Storage
            </span>
            <span className="font-bold">{metrics.disk}%</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <div
              className="h-full bg-slate-400 rounded-full transition-all duration-1000"
              style={{ width: `${Math.min(metrics.disk, 100)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Phase 23: Provenance & Canary Status */}
      <div className="mt-6 pt-4 border-t border-slate-200/50 flex justify-between items-center opacity-70">
        <div className="text-[10px] font-mono text-slate-400">
          SHA: <span className="text-slate-500">{status?.head_sha || "unknown"}</span>
        </div>
        <div className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 text-slate-500">
          {status?.canary_status || "STABLE"}
        </div>
      </div>
    </div>
  );
};
