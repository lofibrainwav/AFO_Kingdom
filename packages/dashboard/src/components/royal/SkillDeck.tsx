"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import useSWR from "swr";
import clsx from "clsx";

const fetcher = (url: string) => fetch(url).then(r => r.json());

interface Skill {
  id: string;
  name: string;
  category: string;
  status: string;
  philosophy_score: number;
}

export default function SkillDeck() {
  const [executing, setExecuting] = useState<string | null>(null);
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";
  const { data, error } = useSWR(`${API_BASE}/api/skills/list`, fetcher);

  const skills: Skill[] = data?.skills || [];

  const handleDryRun = (skillId: string) => {
    setExecuting(skillId);
    // Simulate execution call to backend in future
    setTimeout(() => setExecuting(null), 2000);
  };

  const getCategoryColor = (cat: string) => {
      switch(cat) {
          case 'truth': return 'bg-indigo-500';
          case 'goodness': return 'bg-emerald-500';
          case 'beauty': return 'bg-purple-500'; 
          case 'serenity': return 'bg-sky-500';
          case 'eternity': return 'bg-slate-500';
          default: return 'bg-slate-400';
      }
  };

  if (!data && !error) return <div className="p-4 text-xs text-slate-400">Loading Royal Skills...</div>;

  return (
    <div className="flex overflow-x-auto pb-8 pt-4 gap-6 scrollbar-hide snap-x px-4 h-full items-center">
      {skills.map((skill, index) => (
        <motion.div
           key={skill.id}
           className="neu-card min-w-[200px] w-[200px] flex-shrink-0 flex flex-col p-4 snap-center relative overflow-hidden group h-[280px]"
           animate={{
             y: [0, -10, 0],
             rotate: [0, 1, -1, 0]
           }}
           transition={{
             duration: 4,
             repeat: Infinity,
             delay: index * 0.1,
             ease: "easeInOut"
           }}
           whileHover={{ scale: 1.05, zIndex: 10, rotate: 0 }}
        >
          {/* Header Color Block */}
          <div className={clsx("absolute top-0 left-0 right-0 h-16 opacity-20 transition-opacity group-hover:opacity-40", getCategoryColor(skill.category))} />
          
          <div className="z-10 mt-2">
            <h3 className="text-lg font-bold text-slate-700 leading-tight">{skill.name}</h3>
            <div className="flex gap-2 mt-2 flex-wrap">
               <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/40 border border-white/60 text-slate-500 uppercase tracking-wider">{skill.category}</span>
            </div>
          </div>
          
          <div className="mt-4 flex-1">
              <div className="text-[10px] text-slate-500 leading-relaxed font-light">
                  {(skill as any).description}
              </div>
          </div>

          <div className="mt-auto pt-4 z-10">
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => handleDryRun(skill.id)}
              disabled={!!executing}
              className={clsx(
                "w-full py-2 rounded-lg text-xs font-bold transition-all shadow-md border border-white/50",
                executing === skill.id 
                  ? "bg-slate-100 text-slate-400 cursor-not-allowed" 
                  : "bg-gradient-to-r from-slate-100 to-white text-slate-600 hover:from-white hover:to-slate-50"
              )}
            >
              {executing === skill.id ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-400 animate-ping"/>
                  RUNNING...
                </span>
              ) : (
                "DRY RUN"
              )}
            </motion.button>
          </div>
          
          {/* Glass Shine Effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-white/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"/>
        </motion.div>
      ))}
    </div>
  );
}
