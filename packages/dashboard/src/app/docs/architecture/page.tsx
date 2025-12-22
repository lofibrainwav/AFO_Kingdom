"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { RoyalArchitecture } from "@/components/royal/RoyalArchitecture";

export default function ArchitecturePage() {
  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400">
                🏛️ 시스템 아키텍처
              </h1>
              <p className="text-slate-500 text-lg mt-2">4계층 아키텍처와 데이터 플로우</p>
            </div>
            <Link
              href="/docs"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              ← 문서 목록
            </Link>
          </div>
        </motion.header>

        {/* 4-Layer Architecture */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-12"
        >
          <h2 className="text-2xl font-bold text-slate-700 mb-6">4계층 아키텍처</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                layer: "Presentation",
                description: "Next.js Dashboard, UI 컴포넌트",
                color: "from-blue-500/20 to-cyan-500/20",
                border: "border-blue-500/40",
              },
              {
                layer: "Application",
                description: "API 라우터, 비즈니스 로직",
                color: "from-purple-500/20 to-pink-500/20",
                border: "border-purple-500/40",
              },
              {
                layer: "Domain",
                description: "도메인 모델, 엔티티",
                color: "from-green-500/20 to-emerald-500/20",
                border: "border-green-500/40",
              },
              {
                layer: "Infrastructure",
                description: "DB, Redis, Qdrant, Ollama",
                color: "from-orange-500/20 to-red-500/20",
                border: "border-orange-500/40",
              },
            ].map((layer, index) => (
              <motion.div
                key={layer.layer}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className={`bg-gradient-to-br ${layer.color} backdrop-blur-sm rounded-2xl p-6 border-2 ${layer.border} shadow-inner`}
              >
                <div className="text-3xl font-bold text-slate-700 mb-2">{index + 1}</div>
                <h3 className="text-xl font-bold text-slate-700 mb-2">{layer.layer}</h3>
                <p className="text-slate-500 text-sm">{layer.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Data Flow */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-12 bg-white/30 backdrop-blur-sm rounded-3xl p-8 border border-white/40"
        >
          <h2 className="text-2xl font-bold text-slate-700 mb-6">데이터 플로우</h2>
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center text-slate-700 font-bold">
                1
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-slate-700">사용자 요청</h3>
                <p className="text-slate-500 text-sm">Next.js Dashboard (포트 3000)</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-500/20 rounded-full flex items-center justify-center text-slate-700 font-bold">
                2
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-slate-700">API 라우터</h3>
                <p className="text-slate-500 text-sm">FastAPI (포트 8010)</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center text-slate-700 font-bold">
                3
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-slate-700">도메인 로직</h3>
                <p className="text-slate-500 text-sm">Chancellor Graph, Trinity Score</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-orange-500/20 rounded-full flex items-center justify-center text-slate-700 font-bold">
                4
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-slate-700">인프라</h3>
                <p className="text-slate-500 text-sm">PostgreSQL, Redis, Qdrant, Ollama</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Royal Architecture Component */}
        <RoyalArchitecture />
      </div>
    </div>
  );
}
