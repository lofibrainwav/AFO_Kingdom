'use client';

import React from 'react';
import { Layout, ShieldCheck } from 'lucide-react';
import { ARCH_LAYERS, CHANCELLOR_FLOW } from '../../config/royal_constants';

export const RoyalArchitecture: React.FC = () => {
  return (
    <section className="py-8 text-slate-700">
      <div className="flex items-center gap-4 mb-8">
        <h2 className="text-xl font-bold text-slate-600">SYSTEM ARCHITECTURE (v100.0)</h2>
        <div className="h-[1px] flex-1 bg-slate-300"/>
      </div>

      {/* 1. Hierarchy Tree (Simplified Visual) */}
      <div className="mb-12">
        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Kingdom Command Structure</h3>
        <div className="flex flex-col items-center gap-4">
          {/* Commander */}
          <div className="p-4 bg-slate-800 text-white rounded-xl shadow-lg border border-slate-600 w-64 text-center font-bold relative z-10">
            👑 Commander (User)
          </div>
          <div className="h-8 w-[1px] bg-slate-400"></div>
          
          {/* Chancellor */}
          <div className="p-4 bg-indigo-600 text-white rounded-xl shadow-lg border border-indigo-500 w-64 text-center font-bold relative z-10">
            📜 Chancellor (AI Agent)
            <div className="text-xs font-normal opacity-80 mt-1">Cursor / Antigravity</div>
          </div>
          <div className="h-8 w-[1px] bg-slate-400"></div>

          {/* Strategists */}
          <div className="grid grid-cols-3 gap-4 w-full max-w-2xl">
            <div className="p-3 bg-blue-100 border border-blue-200 rounded-lg text-center">
              <div className="font-bold text-blue-800">Zhuge Liang</div>
              <div className="text-xs text-blue-600">Truth 35%</div>
            </div>
            <div className="p-3 bg-green-100 border-green-200 rounded-lg text-center">
              <div className="font-bold text-green-800">Sima Yi</div>
              <div className="text-xs text-green-600">Goodness 35%</div>
            </div>
            <div className="p-3 bg-purple-100 border-purple-200 rounded-lg text-center">
              <div className="font-bold text-purple-800">Zhou Yu</div>
              <div className="text-xs text-purple-600">Beauty 20%</div>
            </div>
          </div>
          
          <div className="h-8 w-[1px] bg-slate-400"></div>

          {/* Scholars / API Wallet */}
          <div className="p-3 border border-dashed border-slate-400 rounded-xl bg-slate-50 w-full max-w-2xl text-center">
             <div className="text-xs font-bold text-slate-400 mb-2">API WALLET & SCHOLARS</div>
             <div className="flex justify-center gap-4 flex-wrap">
                <span className="px-3 py-1 bg-white rounded shadow-sm text-xs font-mono">Bangtong (Codex)</span>
                <span className="px-3 py-1 bg-white rounded shadow-sm text-xs font-mono">Jaryong (Claude)</span>
                <span className="px-3 py-1 bg-white rounded shadow-sm text-xs font-mono">Yukson (Gemini)</span>
                <span className="px-3 py-1 bg-white rounded shadow-sm text-xs font-mono">Yeongdeok (Ollama)</span>
             </div>
          </div>
        </div>
      </div>

      {/* 2. 4-Layer Architecture */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm">
          <h3 className="flex items-center gap-2 font-bold mb-4 text-slate-600">
            <Layout className="w-5 h-5"/> 4-Layer Hierarchy
          </h3>
          <div className="space-y-3">
            {ARCH_LAYERS.map((layer, idx) => (
               <LayerCard key={idx} icon={layer.icon} title={layer.title} desc={layer.desc} color={layer.color} />
            ))}
          </div>
        </div>

        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm">
          <h3 className="flex items-center gap-2 font-bold mb-4 text-slate-600">
             <ShieldCheck className="w-5 h-5"/> Chancellor Logic Flow
          </h3>
          <div className="relative pl-6 border-l-2 border-indigo-200 space-y-6">
            {CHANCELLOR_FLOW.map((step, idx) => (
                <FlowStep key={idx} title={step.title} desc={step.desc} highlight={step.highlight} />
            ))}
          </div>
        </div>
      </div>

    </section>
  );
};

const LayerCard = ({ icon: Icon, title, desc, color }: any) => (
  <div className="flex items-center gap-4 p-3 bg-white rounded-lg border border-slate-100 shadow-sm">
    <div className={`p-2 rounded-md text-white ${color}`}>
      <Icon size={16} />
    </div>
    <div>
      <div className="font-bold text-sm text-slate-700">{title}</div>
      <div className="text-xs text-slate-400">{desc}</div>
    </div>
  </div>
);

const FlowStep = ({ title, desc, highlight }: any) => (
  <div className="relative">
    <div className={`absolute -left-[29px] top-1 w-3 h-3 rounded-full border-2 border-white ${highlight ? 'bg-indigo-500 ring-2 ring-indigo-200' : 'bg-slate-300'}`} />
    <div className={`text-sm font-bold ${highlight ? 'text-indigo-600' : 'text-slate-600'}`}>{title}</div>
    <div className="text-xs text-slate-400">{desc}</div>
  </div>
);
