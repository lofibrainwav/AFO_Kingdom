"use client";

import { motion } from "framer-motion";

interface Organ {
  name: string;
  score: number;
  metric: string;
}

interface OrgansMonitorProps {
  organs?: Organ[];
}

const DEFAULT_ORGANS = [
  { name: "Heart", score: 0, metric: "Connecting..." },
  { name: "Brain", score: 0, metric: "Connecting..." },
  { name: "Lungs", score: 0, metric: "Connecting..." },
  { name: "Stomach", score: 0, metric: "Connecting..." },
  { name: "Eyes", score: 0, metric: "Connecting..." },
];

export default function OrgansMonitor({ organs = DEFAULT_ORGANS }: OrgansMonitorProps) {
  return (
    <div className="grid grid-cols-5 gap-4">
      {organs.map((organ, index) => (
        <motion.div
          key={organ.name}
          className="neu-card flex flex-col items-center justify-center p-4 min-h-[140px]"
          animate={{ 
            y: [0, -5, 0],
          }}
          transition={{ 
            duration: 3, 
            repeat: Infinity,
            delay: index * 0.2, // Stagger effect
            ease: "easeInOut"
          }}
          whileHover={{ scale: 1.05, y: -10 }}
        >
          {/* Organ Icon / Visualization */}
          <div className="relative w-12 h-12 mb-3 items-center justify-center flex">
             <svg className="w-full h-full text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
               {/* Simple Placeholder Paths based on name */}
               {organ.name === "Heart" && <path d="M20.8 4.6a5.5 5.5 0 00-7.7 0l-1.1 1-1-1a5.5 5.5 0 00-7.8 7.8l1 1 7.8 7.8 7.8-7.7 1-1.1a5.5 5.5 0 000-7.8z" />}
               {organ.name === "Brain" && <path d="M9.5 2A2.5 2.5 0 0112 4.5v15a2.5 2.5 0 01-4.96.44 2.5 2.5 0 01-2.96-3.08 3 3 0 01-.34-5.58 2.5 2.5 0 011.32-4.24 2.5 2.5 0 01.44-5.04zM14.5 2 A2.5 2.5 0 0012 4.5v15a2.5 2.5 0 004.96.44 2.5 2.5 0 002.96-3.08 3 3 0 00.34-5.58 2.5 2.5 0 00-1.32-4.24 2.5 2.5 0 00-.44-5.04z" />}
               {!["Heart", "Brain"].includes(organ.name) && <circle cx="12" cy="12" r="9" />}
             </svg>
             {/* Pulse Ring */}
             <motion.div 
               className="absolute inset-0 rounded-full border-2 border-emerald-500/30"
               animate={{ scale: [1, 1.5], opacity: [1, 0] }}
               transition={{ duration: 1.5, repeat: Infinity, delay: index * 0.2 }}
             />
          </div>

          <h4 className="text-sm font-bold text-slate-600">{organ.name}</h4>
          <span className="text-[10px] text-slate-400 mb-2">{organ.metric}</span>

          {/* Health Bar */}
          <div className="w-full bg-slate-200/50 rounded-full h-1.5 overflow-hidden">
            <motion.div 
              className={clsx(
                "h-full rounded-full",
                organ.score > 90 ? "bg-emerald-400" : (organ.score > 70 ? "bg-amber-400" : "bg-rose-400")
              )}
              initial={{ width: 0 }}
              animate={{ width: `${organ.score}%` }}
              transition={{ duration: 1 }}
            />
          </div>
        </motion.div>
      ))}
    </div>
  );
}

// Helper utility for classnames
import clsx from "clsx";
