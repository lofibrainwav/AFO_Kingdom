"use client";

import { motion } from "framer-motion";
import { SectionCard, MermaidDiagramLazy } from "@/components/docs";
import dynamic from "next/dynamic";

// ChancellorStream도 지연 로딩
const ChancellorStreamLazy = dynamic(
  () =>
    import("@/components/royal/ChancellorStream").then((mod) => ({
      default: mod.default,
    })),
  {
    loading: () => (
      <div className="p-8 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">스트림 로딩 중...</p>
      </div>
    ),
  }
);

const strategistsMermaid = `graph LR
    Query[사용자 쿼리] --> Zhuge[제갈량<br/>眞 Truth]
    Query --> Sima[사마의<br/>善 Goodness]
    Query --> Zhou[주유<br/>美 Beauty]
    Zhuge --> Trinity[Trinity Score<br/>계산]
    Sima --> Trinity
    Zhou --> Trinity
    Trinity --> Decision{의사결정}
    Decision -->|Score≥90 & Risk≤10| AutoRun[AUTO_RUN]
    Decision -->|조건 미충족| Ask[ASK_COMMANDER]`;

const tigersMermaid = `stateDiagram-v2
    [*] --> Constitutional: 쿼리 입력
    Constitutional --> ZhugeNode: 헌법 검증 통과
    Constitutional --> Blocked: 헌법 위반
    ZhugeNode --> SimaNode: Truth 평가
    SimaNode --> ZhouNode: Goodness 검토
    ZhouNode --> TrinityNode: Beauty 최적화
    TrinityNode --> DecisionGate: Trinity Score 계산
    DecisionGate --> TigersNode: AUTO_RUN
    DecisionGate --> AskCommander: ASK
    TigersNode --> HistorianNode: 실행 완료
    HistorianNode --> [*]: 기록 저장
    AskCommander --> [*]: 사용자 승인 대기`;

const tigers = [
  { name: "관우", pillar: "眞", role: "사실 검증 및 무결성 수호", interface: "truth_guard" },
  { name: "장비", pillar: "善", role: "위험 차단 및 실행 승인", interface: "goodness_gate" },
  { name: "조운", pillar: "美", role: "우아한 구현 및 미학 집행", interface: "beauty_craft" },
  { name: "마초", pillar: "孝", role: "자동 배포 및 운영 마찰 제거", interface: "serenity_deploy" },
  { name: "황충", pillar: "永", role: "기록 보존 및 역사 기록", interface: "eternity_log" },
];

export default function ChancellorPage() {
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
            승상 시스템 구도
          </h1>
          <p className="text-slate-500 text-lg">
            3책사 병렬 조율과 5호대장군 실행 구조
          </p>
        </motion.header>

        {/* 3책사 병렬 조율 */}
        <SectionCard title="3책사 병렬 조율" badge="핵심">
          <MermaidDiagramLazy code={strategistsMermaid} title="3책사 의사결정 플로우" />
        </SectionCard>

        {/* 5호대장군 실행 구조 */}
        <SectionCard title="5호대장군 실행 구조" badge="핵심">
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-slate-100 border-b-2 border-slate-300">
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">장군</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">기둥</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">역할</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-slate-700">인터페이스</th>
                </tr>
              </thead>
              <tbody>
                {tigers.map((tiger, index) => (
                  <motion.tr
                    key={tiger.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border-b border-slate-200 hover:bg-slate-50 transition-colors"
                  >
                    <td className="px-4 py-3 text-sm font-semibold text-slate-700">{tiger.name}</td>
                    <td className="px-4 py-3 text-sm text-slate-600">{tiger.pillar}</td>
                    <td className="px-4 py-3 text-sm text-slate-600">{tiger.role}</td>
                    <td className="px-4 py-3 text-sm font-mono text-indigo-600">{tiger.interface}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>

        {/* LangGraph 상태 머신 */}
        <SectionCard title="LangGraph 상태 머신" badge="고급">
          <MermaidDiagramLazy code={tigersMermaid} title="상태 머신 다이어그램" />
        </SectionCard>

        {/* Chancellor Stream */}
        <SectionCard title="실시간 승상 스트림" badge="실시간">
          <div className="min-h-[400px]">
            <ChancellorStreamLazy />
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

