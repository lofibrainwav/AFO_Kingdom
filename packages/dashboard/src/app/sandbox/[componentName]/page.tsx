'use client';

import React, { Suspense } from 'react';
import * as GenUIRegistry from '@/components/genui';
import { useParams } from 'next/navigation';
import { Loader2, AlertTriangle } from 'lucide-react';

export default function SandboxPreviewPage() {
  const params = useParams();
  const componentName = params.componentName as string;

  // Dynamic lookup in registry
  const Component = (GenUIRegistry as any)[componentName];

  if (!Component) {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center text-white p-8">
        <AlertTriangle className="w-16 h-16 text-yellow-500 mb-4" />
        <h1 className="text-2xl font-bold mb-2">Component Not Found</h1>
        <p className="text-gray-400 font-mono text-sm">Target: {componentName}</p>
        <div className="mt-8 p-4 bg-white/5 border border-white/10 rounded-xl max-w-md">
            <p className="text-xs text-gray-500 leading-relaxed">
                Ensure the component has been generated and exported in <code>src/components/genui/index.ts</code>.
                If it was just generated, HMR might take a few seconds to update the registry.
            </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-8 overflow-hidden relative">
        {/* Aesthetic Background */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.05)_0%,transparent_70%)]"></div>
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        
        <div className="relative z-10 w-full max-w-6xl flex flex-col items-center">
            <div className="mb-6 flex items-center gap-2 px-4 py-1.5 bg-indigo-500/10 border border-indigo-500/20 rounded-full">
                <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></div>
                <span className="text-[10px] uppercase tracking-[0.2em] font-black text-indigo-300">
                    Samahwi Vision Preview: {componentName}
                </span>
            </div>
            
            <Suspense fallback={<Loader2 className="w-12 h-12 text-indigo-500 animate-spin" />}>
                <div className="animate-in fade-in zoom-in-95 duration-700">
                    <Component />
                </div>
            </Suspense>

            <div className="mt-12 opacity-30 hover:opacity-100 transition-opacity duration-500 flex flex-col items-center">
                 <p className="text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1">Generated via Phase 9 Self-Expansion Loop</p>
                 <div className="h-[1px] w-48 bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
            </div>
        </div>
    </div>
  );
}
