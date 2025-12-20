'use client';

import { Server, Activity, ArrowUpRight, Cloud } from 'lucide-react';

export function K8sStatusWidget() {
  // Mock data for Phase 17 visualization
  const status = {
    pods: { current: 12, max: 20 },
    nodes: 5,
    memory: '4.2 GB',
    cpu: '3.5 Cores',
    environment: 'GKE (Production)'
  };

  const utilization = Math.round((status.pods.current / status.pods.max) * 100);

  return (
    <div className="glass-card p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-3xl border border-cyan-500/30 shadow-xl relative overflow-hidden group">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-all duration-700"></div>
      
      <div className="flex items-center justify-between mb-6 relative z-10">
        <h3 className="text-xl font-bold text-cyan-300 flex items-center gap-2">
          <Cloud className="w-6 h-6" />
          Cloud Infrastructure
        </h3>
        <div className="flex items-center gap-1 text-xs font-mono text-cyan-400 bg-cyan-900/50 px-2 py-1 rounded border border-cyan-500/30">
          <Activity className="w-3 h-3" />
          SYSTEM_NORMAL
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6 relative z-10">
        <div className="p-4 bg-black/20 rounded-xl border border-cyan-500/10">
          <div className="flex items-center gap-2 text-cyan-200/70 text-sm mb-1">
            <Server className="w-4 h-4" /> Nodes
          </div>
          <div className="text-2xl font-bold text-white relative">
            {status.nodes}
            <span className="text-xs font-normal text-emerald-400 ml-2 bg-emerald-900/30 px-1 rounded absolute top-0 -right-4 translate-x-full">
              Auto-Scaling
            </span>
          </div>
        </div>
        <div className="p-4 bg-black/20 rounded-xl border border-cyan-500/10">
          <div className="flex items-center gap-2 text-cyan-200/70 text-sm mb-1">
            <ArrowUpRight className="w-4 h-4" /> Pods
          </div>
          <div className="text-2xl font-bold text-white">
            {status.pods.current} <span className="text-base font-medium text-white/50">/ {status.pods.max}</span>
          </div>
          <div className="mt-1 h-1.5 w-full bg-cyan-900/30 rounded-full overflow-hidden">
             <div 
               className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all duration-1000"
               style={{ width: `${utilization}%` }}
             ></div>
          </div>
        </div>
      </div>

      <div className="relative z-10">
        <p className="text-center text-white/70 italic text-sm border-t border-cyan-500/20 pt-4">
          "The Kingdom ascends to the Cloud – Infinite Scale, Eternal Peace."
        </p>
      </div>
    </div>
  );
}
