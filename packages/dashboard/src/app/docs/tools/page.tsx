"use client";

import { motion } from "framer-motion";
import { SectionCard } from "@/components/docs";
import SkillDeck from "@/components/royal/SkillDeck";

export default function ToolsPage() {
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
            Skills & 도구
          </h1>
          <p className="text-slate-500 text-lg">
            AFO Kingdom의 19개 스킬 레지스트리
          </p>
        </motion.header>

        {/* Skills Deck */}
        <SectionCard title="스킬 레지스트리" badge="19개">
          <div className="min-h-[400px]">
            <SkillDeck />
          </div>
        </SectionCard>

        {/* Skills Categories */}
        <SectionCard title="스킬 카테고리" badge="참고">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { name: "眞 (Truth)", color: "bg-indigo-500", count: "기술적 확실성" },
              { name: "善 (Goodness)", color: "bg-emerald-500", count: "윤리·안정성" },
              { name: "美 (Beauty)", color: "bg-purple-500", count: "구조적 우아함" },
              { name: "孝 (Serenity)", color: "bg-sky-500", count: "평온 수호" },
              { name: "永 (Eternity)", color: "bg-slate-500", count: "영속성" },
            ].map((category, index) => (
              <motion.div
                key={category.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="p-6 bg-white/50 backdrop-blur-sm rounded-xl border border-white/60 text-center"
              >
                <div className={`w-12 h-12 ${category.color} rounded-full mx-auto mb-3 flex items-center justify-center text-white font-bold text-xl`}>
                  {category.name.charAt(0)}
                </div>
                <h3 className="font-bold text-slate-700 mb-2">{category.name}</h3>
                <p className="text-sm text-slate-600">{category.count}</p>
              </motion.div>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

