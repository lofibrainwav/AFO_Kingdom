'use client';

import React from 'react';
import { useApi } from '@/hooks/useApi';

interface KingdomStatus {
  buildVersion?: string;
  backendStatus?: string;
  generatedAt?: string;
  [key: string]: unknown;
}

export const SystemFingerprintFooter = () => {
  const { data } = useApi<KingdomStatus>('/api/kingdom-status');

  const buildVersion = data?.buildVersion || '---';
  const backendStatus = data?.backendStatus || '---';
  const generatedAt = data?.generatedAt ? new Date(data.generatedAt).toLocaleString() : '---';

  return (
    <footer className="mt-12 w-full border-t border-white/10 pt-6 pb-12">
      <div className="flex flex-col md:flex-row justify-between items-center text-[10px] uppercase tracking-widest text-white/30 font-mono gap-4">
        <div className="flex flex-wrap justify-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-emerald-500/50">BUILD_FINGERPRINT:</span>
            <span className="text-white/60 select-all">{buildVersion}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-emerald-500/50">SOUL_ENGINE_STATUS:</span>
            <span className={`${backendStatus === 'balanced' ? 'text-emerald-400' : 'text-amber-400'} font-bold`}>
              {backendStatus}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-emerald-500/50">LAST_TRUTHFUL_SYNC:</span>
          <span>{generatedAt}</span>
        </div>
      </div>
      <div className="mt-4 text-center">
        <p className="text-[9px] text-white/10 uppercase tracking-tighter">
          眞善美孝永 Five Pillars Architecture • Protected by AntiGravity Sovereign Logic
        </p>
      </div>
    </footer>
  );
};
