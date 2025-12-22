import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ROYAL_PILLARS, TRINITY_FORMULA, AUTORUN_RULE } from '../../config/royal_constants';

import { PillarModal } from './PillarModal';

export const RoyalPhilosophy: React.FC = () => {
  const [activePillar, setActivePillar] = useState<string | null>(null);

  // Global Bridge for "Truth" (User Report Requirement)
  useEffect(() => {
     window.showPillarDetails = (id: string) => setActivePillar(id);
     window.closePillarDetails = () => setActivePillar(null);
     return () => {
         // Cleanup
         // @ts-expect-error - Window property mismatch
         delete window.showPillarDetails;
         // @ts-expect-error - Window property mismatch
         delete window.closePillarDetails;
     }
  }, []);

  return (
    <section className="py-8">
      <div className="flex items-center gap-4 mb-6">
        <h2 className="text-xl font-bold text-slate-600">眞善美孝永 - PHILOSOPHY</h2>
        <div className="h-[1px] flex-1 bg-slate-300"/>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        {ROYAL_PILLARS.map((p) => (
          <motion.div
            key={p.id}
            whileHover={{ y: -5 }}
            onClick={() => setActivePillar(p.id)}
            className={`p-6 rounded-2xl bg-white/70 backdrop-blur-md border ${p.border} shadow-sm cursor-pointer hover:shadow-md transition-all relative overflow-hidden group`}
          >
            <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${p.color}`}>
              <p.icon size={60} />
            </div>
            <div className="text-4xl font-black mb-2 text-slate-700">{p.label}</div>
            <div className={`text-xs font-bold uppercase tracking-wider mb-1 ${p.color}`}>{p.name} ({p.weight})</div>
            <div className="text-sm font-semibold text-slate-600">{p.role}</div>
            <div className="text-xs text-slate-400 mt-1">{p.desc}</div>
          </motion.div>
        ))}
      </div>

      <div className="p-6 rounded-xl bg-slate-200/50 border border-slate-300/50 text-center font-mono text-sm text-slate-600">
        {TRINITY_FORMULA}
        <div className="text-xs text-slate-400 mt-2">
           AUTO_RUN Rule: {AUTORUN_RULE}
        </div>
      </div>

      {/* The Truth Modal */}
      <PillarModal pillarId={activePillar} onClose={() => setActivePillar(null)} />
    </section>
  );
};

