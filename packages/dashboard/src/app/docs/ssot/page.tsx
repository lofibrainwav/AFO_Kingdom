"use client";

import { motion } from "framer-motion";
import { SectionCard } from "@/components/docs";

const personas = [
  { persona: "승상", codename: "Chancellor", role: "3책사 병렬 조율, 웹 오케스트레이터" },
  { persona: "제갈량", codename: "Zhuge Liang", role: "眞 35% - 아키텍처·전략·개발" },
  { persona: "사마의", codename: "Sima Yi", role: "善 35% - 윤리·안정·게이트" },
  { persona: "주유", codename: "Zhou Yu", role: "美 20% - 서사·UX·취향정렬" },
  { persona: "방통", codename: "Bangtong", role: "Codex - 구현·실행·프로토타이핑" },
  { persona: "자룡", codename: "Jaryong", role: "Claude - 논리 검증·리팩터링" },
  { persona: "육손", codename: "Yukson", role: "Gemini - 전략·철학·큰 그림" },
  { persona: "영덕", codename: "Yeongdeok", role: "Ollama - 설명·보안·아카이빙" },
];

export default function SSOTPage() {
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
            SSOT (Single Source of Truth)
          </h1>
          <p className="text-slate-500 text-lg">
            TRINITY_OS_PERSONAS.yaml - 웹·깃·로컬의 유일한 페르소나/명칭 정본
          </p>
        </motion.header>

        {/* TRINITY_OS_PERSONAS.yaml */}
        <SectionCard title="TRINITY_OS_PERSONAS.yaml" badge="정본">
          <p className="mb-6 text-slate-600">
            이 파일이 웹·깃·로컬의 유일한 페르소나/명칭 정본입니다.
          </p>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-slate-100 border-b-2 border-slate-300">
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">페르소나</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">코드명</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">역할</th>
                </tr>
              </thead>
              <tbody>
                {personas.map((persona, index) => (
                  <motion.tr
                    key={persona.codename}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="border-b border-slate-200 hover:bg-slate-50 transition-colors"
                  >
                    <td className="px-4 py-3 text-sm font-semibold text-slate-700">{persona.persona}</td>
                    <td className="px-4 py-3 text-sm font-mono text-indigo-600">{persona.codename}</td>
                    <td className="px-4 py-3 text-sm text-slate-600">{persona.role}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>

        {/* SSOT 파일 목록 */}
        <SectionCard title="SSOT 파일 목록" badge="참고">
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
              <div className="font-bold text-slate-700 mb-2">1순위: docs/AFO_ROYAL_LIBRARY.md</div>
              <p className="text-sm text-slate-600">
                왕국 원칙/헌법, 41가지 원칙
              </p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
              <div className="font-bold text-slate-700 mb-2">2순위: docs/AFO_CHANCELLOR_GRAPH_SPEC.md</div>
              <p className="text-sm text-slate-600">
                Trinity Score / Routing 규칙
              </p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
              <div className="font-bold text-slate-700 mb-2">3순위: docs/AFO_EVOLUTION_LOG.md</div>
              <p className="text-sm text-slate-600">
                결정/변경 이력
              </p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
              <div className="font-bold text-slate-700 mb-2">4순위: docs/AFO_FRONTEND_ARCH.md</div>
              <p className="text-sm text-slate-600">
                UI/Frontend 규율
              </p>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
              <div className="font-bold text-slate-700 mb-2">5순위: docs/CURSOR_MCP_SETUP.md</div>
              <p className="text-sm text-slate-600">
                MCP 도구/서버 가이드
              </p>
            </div>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

