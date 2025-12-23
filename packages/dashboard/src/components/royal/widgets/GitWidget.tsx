"use client";

import { GitBranch, GitCommit } from "lucide-react";

export const GitWidget = () => {
  return (
    <div className="neu-card min-h-[200px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-600 flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-orange-500" />
          GIT REPOSITORY
        </h3>
        <span className="px-2 py-1 text-xs font-bold rounded-full bg-blue-100 text-blue-700">
          main
        </span>
      </div>

      <div className="space-y-3">
        <div className="flex items-center gap-3 p-3 bg-slate-100/50 rounded-xl border border-slate-200/50">
          <GitCommit className="w-4 h-4 text-slate-400" />
          <div className="flex-1">
            <div className="text-xs font-mono text-slate-400">SHA: a8f9c2</div>
            <div className="text-xs font-medium text-slate-700">feat: Project Genesis Init</div>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-500">Status</span>
          <span className="text-emerald-600 font-bold flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Clean
          </span>
        </div>
      </div>
    </div>
  );
};
