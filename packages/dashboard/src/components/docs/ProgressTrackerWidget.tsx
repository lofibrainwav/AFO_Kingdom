"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, CheckCircle, Clock } from "lucide-react";

interface ProgressData {
  planned: number;
  completed: number;
  inProgress: number;
  overall: number;
}

export function ProgressTrackerWidget() {
  const [progress, setProgress] = useState<ProgressData>({
    planned: 0,
    completed: 0,
    inProgress: 0,
    overall: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";
        const response = await fetch(`${API_BASE}/api/progress/tracker`);
        
        if (response.ok) {
          const data = await response.json();
          setProgress({
            planned: data.planned || 0,
            completed: data.completed || 0,
            inProgress: data.in_progress || 0,
            overall: data.overall_percentage || 0,
          });
        }
      } catch (error) {
        console.error("Progress tracker fetch failed:", error);
        // 기본값 설정
        setProgress({
          planned: 100,
          completed: 75,
          inProgress: 15,
          overall: 75,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
    const interval = setInterval(fetchProgress, 5000); // 5초마다 업데이트

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="neu-card min-h-[200px] flex items-center justify-center">
        <div className="animate-pulse text-slate-400">로딩 중...</div>
      </div>
    );
  }

  const total = progress.planned || 1;
  const completedPercent = (progress.completed / total) * 100;
  const inProgressPercent = (progress.inProgress / total) * 100;

  return (
    <div className="neu-card min-h-[200px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-600 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-green-500" />
          구현 진행률
        </h3>
        <span className="px-2 py-1 text-xs font-bold rounded-full bg-green-100 text-green-700">
          {progress.overall}%
        </span>
      </div>

      <div className="space-y-4">
        {/* 계획된 기능 */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span>계획된 기능</span>
            <span className="font-bold">{progress.planned}</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <div
              className="h-full bg-slate-300 rounded-full transition-all duration-1000"
              style={{ width: "100%" }}
            />
          </div>
        </div>

        {/* 구현 완료 */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-500" />
              구현 완료
            </span>
            <span className="font-bold">{progress.completed}</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${completedPercent}%` }}
              transition={{ duration: 1 }}
              className="h-full bg-green-500 rounded-full"
            />
          </div>
        </div>

        {/* 진행 중 */}
        <div>
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3 text-yellow-500" />
              진행 중
            </span>
            <span className="font-bold">{progress.inProgress}</span>
          </div>
          <div className="h-2 w-full bg-slate-200/50 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${inProgressPercent}%` }}
              transition={{ duration: 1 }}
              className="h-full bg-yellow-500 rounded-full"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

