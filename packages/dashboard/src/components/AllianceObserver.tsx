'use client';

import React, { useEffect, useState } from 'react';
import { Shield, Globe, Activity, AlertTriangle, CheckCircle2, Server } from 'lucide-react';

interface AllianceMember {
  id: str;
  name: str;
  type: string;
  status: string;
  dns_reachable?: boolean;
  observed_at?: string;
  description?: string;
}

interface ObservationReport {
  timestamp: string | null;
  alliances: AllianceMember[];
  source: string;
}

export const AllianceObserver: React.FC = () => {
  const [report, setReport] = useState<ObservationReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:8010/api/alliances/status');
      if (!response.ok) throw new Error('Failed to fetch alliance status');
      const data = await response.json();
      setReport(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // 30s refresh
    return () => clearInterval(interval);
  }, []);

  if (loading && !report) {
    return (
      <div className="p-6 bg-slate-900/50 rounded-xl border border-slate-800 animate-pulse">
        <div className="h-6 w-48 bg-slate-800 rounded mb-4" />
        <div className="space-y-3">
          {[1, 2, 3].map(i => <div key={i} className="h-12 bg-slate-800/50 rounded" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-slate-900/40 backdrop-blur-md rounded-2xl border border-slate-800/50 shadow-2xl relative overflow-hidden group">
      {/* Background Glow */}
      <div className="absolute -top-24 -right-24 w-48 h-48 bg-blue-500/10 blur-3xl rounded-full group-hover:bg-blue-500/20 transition-all duration-700" />
      
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-500/20 rounded-lg">
            <Globe className="w-5 h-5 text-blue-400" />
          </div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Alliance Observer</h2>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-slate-800/50 rounded-full border border-slate-700/50">
          <Activity className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span className="text-[10px] uppercase tracking-widest text-slate-400 font-semibold">Live Monitoring</span>
        </div>
      </div>

      {error ? (
        <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">
          <AlertTriangle className="w-5 h-5" />
          <p>{error}</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {report?.alliances.map((member) => (
            <div 
              key={member.id}
              className={`p-4 rounded-xl border transition-all duration-300 ${
                member.dns_reachable 
                  ? 'bg-slate-800/30 border-slate-700/50 hover:border-emerald-500/30' 
                  : 'bg-red-500/5 border-red-500/10 hover:border-red-500/30'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`p-2 rounded-lg ${member.dns_reachable ? 'bg-emerald-500/10' : 'bg-red-500/10'}`}>
                    {member.type === 'external_api' ? (
                      <Globe className={`w-4 h-4 ${member.dns_reachable ? 'text-emerald-400' : 'text-red-400'}`} />
                    ) : (
                      <Server className={`w-4 h-4 ${member.dns_reachable ? 'text-emerald-400' : 'text-red-400'}`} />
                    )}
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-200">{member.name}</h3>
                    <p className="text-[10px] text-slate-500 uppercase tracking-tighter">{member.type.replace('_', ' ')}</p>
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-1">
                  <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-[10px] font-bold ${
                    member.dns_reachable 
                      ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                      : 'bg-red-500/10 border-red-500/20 text-red-400'
                  }`}>
                    {member.dns_reachable ? <CheckCircle2 className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                    {member.dns_reachable ? 'DNS REACHABLE' : 'DNS UNREACHABLE'}
                  </div>
                  {member.observed_at && (
                    <span className="text-[9px] text-slate-600 font-mono">
                      {new Date(member.observed_at).toLocaleTimeString()}
                    </span>
                  )}
                </div>
              </div>
              
              {member.description && (
                <div className="mt-3 pt-3 border-t border-slate-700/30">
                  <p className="text-[11px] text-slate-400 leading-relaxed italic">"{member.description}"</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="mt-6 flex items-center justify-between text-[10px] text-slate-500 font-medium">
        <span>Source: {report?.source.toUpperCase()}</span>
        <span>Last Sync: {report?.timestamp ? new Date(report.timestamp).toLocaleTimeString() : 'Never'}</span>
      </div>
    </div>
  );
};
