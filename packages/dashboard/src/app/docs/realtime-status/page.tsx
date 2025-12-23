"use client";

import { motion } from "framer-motion";
import { SectionCard } from "@/components/docs";
import { GitWidget } from "@/components/royal/widgets/GitWidget";
import { SystemStatusWidget } from "@/components/royal/widgets/SystemStatusWidget";
import { ProgressTrackerWidget } from "@/components/docs/ProgressTrackerWidget";
import { OverloadMonitorWidget } from "@/components/docs/OverloadMonitorWidget";

export default function RealtimeStatusPage() {
  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 mb-4">
            📊 실시간 상태 대시보드
          </h1>
          <p className="text-slate-500 text-lg">
            Git 상태, 구현 진행률, 시스템 부하를 실시간으로 모니터링합니다.
          </p>
        </motion.header>

        {/* 위젯 그리드 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Git 상태 위젯 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <GitWidget />
          </motion.div>

          {/* 진행률 추적 위젯 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <ProgressTrackerWidget />
          </motion.div>

          {/* 시스템 부하 위젯 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <OverloadMonitorWidget />
          </motion.div>
        </div>

        {/* 시스템 상태 위젯 (전체 너비) */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <SystemStatusWidget />
        </motion.div>
      </div>
    </div>
  );
}

