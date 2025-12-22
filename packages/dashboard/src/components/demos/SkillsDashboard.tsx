// packages/dashboard/src/components/demos/SkillsDashboard.tsx
// (SWR advanced features AFO 적용)
// 🧭 Trinity Score: 眞90% 善95% 美99% 孝100%

import React, { Suspense } from 'react';
import useSWR, { useSWRConfig } from 'swr';
import { logInfo } from '@/lib/logger';

// === Types ===
interface Skill {
  id: string;
  name: string;
  level: number;
  category: string;
}

// === Fetcher with generic typing ===
const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch data');
  return res.json();
};

// === SWR Configuration Component (Optional Wrapper) ===
// In a real app, wrap _app.tsx with SWRConfig
import { SWRConfig } from 'swr';

export const GlobalSWRConfig = ({ children }: { children: React.ReactNode }) => (
  <SWRConfig 
    value={{
      refreshInterval: 0, // Disable polling by default for this demo
      fetcher: fetcher,
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      suspense: true, // Enable React Suspense mode
    }}
  >
    {children}
  </SWRConfig>
);

// === Sub-component: Skills List (Suspense-enabled) ===
function SkillsList() {
  // Suspense mode: useSWR will suspend (throw promise) if data is missing
  const { data } = useSWR<Skill[]>('/api/skills', {
     // Local overrides
     dedupingInterval: 2000, 
  });

  if (!data) return null; // Should be handled by Suspense, but typescript safety

  return (
    <ul className="space-y-2">
      {data.map((skill) => (
        <li key={skill.id} className="p-3 bg-white/5 rounded-lg border border-white/10 hover:border-gold/50 transition-colors">
          <div className="flex justify-between items-center">
            <span className="font-medium text-white">{skill.name}</span>
            <span className="text-xs text-white/60 px-2 py-1 bg-white/10 rounded">Lv.{skill.level}</span>
          </div>
        </li>
      ))}
    </ul>
  );
}

// === Main Component: Skills Dashboard ===
export default function SkillsDashboard() {
  const { mutate } = useSWRConfig();

  // Optimistic Update Handler
  const handleLevelUp = async () => {
    // 1. Define optimistic data
    const optimisticData = (currentSkills: Skill[] = []) => {
      return currentSkills.map(s => s.id === '1' ? { ...s, level: s.level + 1 } : s);
    };

    // 2. Mutate immediately with optimistic data
    // mutate(key, data, revalidate)
    mutate('/api/skills', optimisticData, false);

    try {
        // 3. Perform actual API call
        // await api.levelUpSkill('1');
        logInfo("API Call Simulated");
        
        // 4. Trigger revalidation to ensure truth
        mutate('/api/skills');
    } catch {
        // 5. Rollback automatically handled by SWR if promise fails? 
        // Actually manual rollback is often clearer or just revalidate
        mutate('/api/skills');
    }
  };

  return (
    <div className="p-6 bg-slate-900 rounded-xl max-w-md mx-auto border border-indigo-500/20 shadow-2xl backdrop-blur-md">
      <h2 className="text-2xl font-bold mb-4 bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
        Kingdom Skills Matrix
      </h2>
      
      {/* Suspense Boundary for SWR */}
      <Suspense fallback={
        <div className="animate-pulse space-y-3">
            <div className="h-10 bg-white/5 rounded"></div>
            <div className="h-10 bg-white/5 rounded"></div>
        </div>
      }>
        <SkillsList />
      </Suspense>

      <div className="mt-6 pt-4 border-t border-white/10">
        <button 
          onClick={handleLevelUp}
          className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-all active:scale-95 font-medium shadow-lg shadow-indigo-500/20"
        >
          🔮 Optimistic Level Up (Mutation)
        </button>
      </div>
      
      <div className="mt-2 text-xs text-center text-white/40">
        Powered by Stale-While-Revalidate Strategy
      </div>
    </div>
  );
}
