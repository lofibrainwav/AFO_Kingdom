"use client";

import { motion } from "framer-motion";
import { GitCommit, GitGraph, Clock, ChevronRight } from "lucide-react";
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

interface Commit {
  hash: string;
  parent: string;
  author: string;
  date: string;
  message: string;
}

interface GitHistoryResponse {
  status: string;
  count: number;
  history: Commit[];
}

export function KingdomHistoryWidget() {
  const { data, error, isLoading } = useSWR<GitHistoryResponse>(
    "/api/proxy/git/history?limit=50",
    fetcher
  );

  if (isLoading) {
    return (
      <div className="w-full h-96 bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-6 shadow-xl flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
      </div>
    );
  }

  if (error || !data || data.status !== "success") {
    return (
      <div className="w-full h-48 bg-red-50/10 backdrop-blur-md rounded-3xl border border-red-200 p-6 flex items-center justify-center text-red-400">
        <p>Failed to load Kingdom Chronicles.</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-6 shadow-xl overflow-hidden flex flex-col h-[500px]">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 bg-indigo-500/20 rounded-xl">
          <GitGraph className="w-6 h-6 text-indigo-400" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-slate-700">왕국 연대기 (Kingdom Chronicles)</h3>
          <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">
            IMMUTABLE HISTORY
          </p>
        </div>
        <div className="ml-auto flex items-center gap-2 text-xs font-mono text-slate-500 bg-slate-200/50 px-3 py-1 rounded-full">
            <Clock className="w-3 h-3" />
            <span>Latest: {data.history[0]?.hash.substring(0, 7)}</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-4 scrollbar-thin scrollbar-thumb-indigo-200 scrollbar-track-transparent">
        {data.history.map((commit, index) => (
          <motion.div
            key={commit.hash}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className="group relative pl-8 border-l-2 border-slate-300 hover:border-indigo-400 transition-colors"
          >
            <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-slate-200 border-2 border-white group-hover:bg-indigo-500 transition-colors" />
            
            <div className="bg-white/40 p-4 rounded-xl hover:bg-white/60 transition-all cursor-default border border-transparent hover:border-indigo-100/50">
                <div className="flex justify-between items-start mb-1">
                    <span className="font-bold text-slate-700 text-sm line-clamp-1">
                        {commit.message}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400 shrink-0">
                        {commit.date.split("T")[0]}
                    </span>
                </div>
                <div className="flex justify-between items-center text-xs text-slate-500">
                    <div className="flex items-center gap-2">
                        <span className="font-medium text-indigo-600/80">{commit.author}</span>
                        <span className="font-mono text-[10px] opacity-50">{commit.hash.substring(0, 7)}</span>
                    </div>
                </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
