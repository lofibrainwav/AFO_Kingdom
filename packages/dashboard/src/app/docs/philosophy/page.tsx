"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { RoyalPhilosophy } from "@/components/royal/RoyalPhilosophy";
import { PillarModal } from "@/components/docs";

export default function PhilosophyPage() {
  const [selectedPillar, setSelectedPillar] = useState<string | null>(null);

  const pillars = [
    {
      id: "truth",
      name: "眞",
      weight: "35%",
      role: "제갈량 - 기술적 확실성",
      description: "Truth: 기술적 확실성, 타입 안전성, 테스트 무결성",
      color: "from-blue-500/20 to-cyan-500/20",
      borderColor: "border-blue-500/40",
    },
    {
      id: "goodness",
      name: "善",
      weight: "35%",
      role: "사마의 - 윤리·안정성",
      description: "Goodness: 윤리/보안/리스크, 비용 최적화, 안전 게이트",
      color: "from-green-500/20 to-emerald-500/20",
      borderColor: "border-green-500/40",
    },
    {
      id: "beauty",
      name: "美",
      weight: "20%",
      role: "주유 - 단순함·우아함",
      description: "Beauty: 구조적 단순함, 모듈화, 일관된 API/UI",
      color: "from-purple-500/20 to-pink-500/20",
      borderColor: "border-purple-500/40",
    },
    {
      id: "serenity",
      name: "孝",
      weight: "8%",
      role: "승상 - 평온 수호",
      description: "Serenity: 형님의 마찰 제거, 자동화, 실패 복구 용이성",
      color: "from-orange-500/20 to-amber-500/20",
      borderColor: "border-orange-500/40",
    },
    {
      id: "eternity",
      name: "永",
      weight: "2%",
      role: "승상 - 영속성",
      description: "Eternity: 재현 가능성, 문서화, 버전/결정 기록",
      color: "from-indigo-500/20 to-violet-500/20",
      borderColor: "border-indigo-500/40",
    },
  ];

  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 mb-4">
            眞善美孝永 - 왕국의 철학
          </h1>
          <p className="text-slate-500 text-lg">AFO Kingdom의 5기둥 철학과 Trinity Score 계산</p>
        </motion.header>

        {/* Pillar Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-12">
          {pillars.map((pillar, index) => (
            <motion.div
              key={pillar.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => setSelectedPillar(pillar.id)}
              className={`bg-gradient-to-br ${pillar.color} backdrop-blur-sm rounded-3xl p-6 border-2 ${pillar.borderColor} shadow-inner cursor-pointer hover:scale-105 transition-all`}
            >
              <div className="text-center">
                <div className="text-5xl font-bold text-slate-700 mb-2">{pillar.name}</div>
                <div className="text-sm text-slate-600 mb-1">{pillar.weight}</div>
                <div className="text-xs text-slate-500">{pillar.role}</div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Trinity Score Formula */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-12 p-8 bg-white/30 backdrop-blur-sm rounded-3xl border border-white/40 shadow-inner"
        >
          <h2 className="text-2xl font-bold text-slate-700 mb-4">Trinity Score 공식</h2>
          <div className="text-center">
            <p className="text-xl font-mono text-slate-700 mb-2">
              Trinity Score = 0.35×眞 + 0.35×善 + 0.20×美 + 0.08×孝 + 0.02×永
            </p>
            <p className="text-slate-500 text-sm">
              AUTO_RUN 조건: Trinity Score ≥ 90 AND Risk Score ≤ 10
            </p>
          </div>
        </motion.div>

        {/* Royal Philosophy Component */}
        <RoyalPhilosophy />

        {/* Pillar Modal */}
        <PillarModal
          isOpen={!!selectedPillar}
          onClose={() => setSelectedPillar(null)}
          pillarName={selectedPillar || ""}
        />
      </div>
    </div>
  );
}
