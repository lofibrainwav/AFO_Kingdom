"use client";

import React from "react";
import { X } from "lucide-react";

interface CommandOverlayProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CommandOverlay({ isOpen, onClose }: CommandOverlayProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-8 bg-black/80 backdrop-blur-md animate-in fade-in duration-500">
      <div className="relative w-full max-w-2xl bg-[#1a1510] border-2 border-[#d4af37] rounded-xl p-6 shadow-[0_0_50px_rgba(212,175,55,0.3)]">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white rounded-full transition-colors"
          aria-label="Close overlay"
        >
          <X className="w-5 h-5" />
        </button>

        <h2 className="text-2xl font-serif font-bold text-[#f5e6d3] mb-4">
          ⚔️ Command Center
        </h2>

        <div className="space-y-4">
          <div className="bg-black/40 border border-[#d4af37]/30 rounded-lg p-4">
            <h3 className="text-sm font-bold text-[#d4af37] mb-2">
              Chancellor Hall Status
            </h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Trinity Score</span>
                <span className="text-emerald-400 font-mono">98%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Risk Level</span>
                <span className="text-amber-400 font-mono">22%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Active Agents</span>
                <span className="text-cyan-400 font-mono">6</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Pending Tasks</span>
                <span className="text-purple-400 font-mono">3</span>
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            <button className="flex-1 bg-[#d4af37] text-black py-2 px-4 rounded font-bold hover:bg-[#f5e6d3] transition-colors">
              Deploy Agent
            </button>
            <button className="flex-1 bg-slate-700 text-white py-2 px-4 rounded font-bold hover:bg-slate-600 transition-colors">
              View Logs
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
