"use client";

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Loader2, Brain, Database, CheckCircle } from 'lucide-react';

interface PillarModalProps {
  pillarId: string | null;
  onClose: () => void;
}

declare global {
  interface Window {
    showPillarDetails: (pillarId: string) => void;
    closePillarDetails: () => void;
  }
}

export const PillarModal: React.FC<PillarModalProps> = ({ pillarId, onClose }) => {
  const [loading, setLoading] = useState(false);
  const [content, setContent] = useState<any>(null);
  const [streamLog, setStreamLog] = useState<string[]>([]);
  
  // Streaming Logic (Simulated for Phase 15, to be connected to Real API)
  useEffect(() => {
    if (pillarId) {
       setLoading(true);
       setStreamLog(["Initializing Chancellor Link..."]);
       
       // Simulate Streaming
       const steps = [
           "Analyzed Query: 'Tell me about " + pillarId + "'",
           "Sequential Thinking: Step 1 [Definition]",
           "Sequential Thinking: Step 2 [Context7 Search]",
           "Found related document: AFO_ROYAL_LIBRARY.md",
           "Synthesizing Ancient Wisdom..."
       ];
       
       let i = 0;
       const interval = setInterval(() => {
           if (i < steps.length) {
               setStreamLog(prev => [...prev, steps[i]]);
               i++;
           } else {
               clearInterval(interval);
               setLoading(false);
               setContent({
                   title: `The Wisdom of ${pillarId.toUpperCase()}`,
                   body: "This pillar represents the core philosophy of AFO Kingdom. It guides our agents to balance Truth, Goodness, Beauty, Serenity, and Eternity."
               });
           }
       }, 800);
       
       return () => clearInterval(interval);
    } else {
        setStreamLog([]);
        setContent(null);
    }
  }, [pillarId]);

  return (
    <AnimatePresence>
      {pillarId && (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
            onClick={onClose}
        >
            <motion.div
                initial={{ scale: 0.95, opacity: 0, y: 20 }}
                animate={{ scale: 1, opacity: 1, y: 0 }}
                exit={{ scale: 0.95, opacity: 0, y: 20 }}
                onClick={(e) => e.stopPropagation()}
                className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden border border-white/60"
            >
                {/* Header */}
                <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                    <h3 className="text-xl font-bold text-slate-700 flex items-center gap-2">
                        <Brain className="w-5 h-5 text-purple-500"/>
                        Chancellor's Analysis: {pillarId.toUpperCase()}
                    </h3>
                    <button onClick={onClose} aria-label="Close" className="p-2 hover:bg-slate-200 rounded-full transition-colors">
                        <X className="w-5 h-5 text-slate-500" />
                    </button>
                </div>
                
                {/* Body */}
                <div className="p-6 min-h-[300px]">
                    {/* Streaming Logs */}
                    <div className="mb-6 space-y-2 font-mono text-xs bg-slate-900 text-green-400 p-4 rounded-lg overflow-y-auto max-h-40">
                         {streamLog.map((log, i) => (
                             <div key={i} className="flex items-center gap-2">
                                 <span className="opacity-50">[{new Date().toLocaleTimeString()}]</span>
                                 {log}
                             </div>
                         ))}
                         {loading && <div className="animate-pulse">_</div>}
                    </div>
                
                    {/* Content */}
                    {!loading && content && (
                         <div className="prose prose-slate">
                             <h4 className="flex items-center gap-2">
                                 <CheckCircle className="w-4 h-4 text-green-500" />
                                 {content.title}
                             </h4>
                             <p>{content.body}</p>
                             <div className="mt-4 p-3 bg-blue-50 text-blue-700 text-sm rounded border border-blue-100 flex items-center gap-2">
                                 <Database className="w-4 h-4"/>
                                 Reference: AFO_ROYAL_LIBRARY.md
                             </div>
                         </div>
                    )}
                </div>
            </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
