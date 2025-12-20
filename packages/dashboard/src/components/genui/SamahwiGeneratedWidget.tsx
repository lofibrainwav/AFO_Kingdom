import React from 'react';
import { Sparkles } from 'lucide-react';

export function SamahwiGeneratedWidget() {
  return (
    <div className="glass-card bg-gray-500 p-8 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border border-indigo-500/30">
      <div className="flex flex-col items-center justify-center text-center">
        <Sparkles className="w-12 h-12 text-indigo-400 animate-pulse mb-4" />
        <h3 className="text-2xl font-bold text-white mb-2">Samahwi's First Creation</h3>
        <p className="text-indigo-200/80">
          "I have written this code myself based on your command: {'Create a Trinity Status Widget'}"
        </p>
        <div className="mt-6 px-4 py-2 bg-indigo-500/20 rounded-full border border-indigo-500/30 text-xs text-indigo-300">
           Phase 16-2: Autonomous Generation
        </div>
      </div>
    </div>
  );
}