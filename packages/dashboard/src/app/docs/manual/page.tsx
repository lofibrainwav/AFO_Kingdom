"use client";

import { motion } from "framer-motion";
import { SectionCard, CodeBlock } from "@/components/docs";
import { BookOpen, CheckCircle } from "lucide-react";

const rules = [
  {
    id: "rule-minus-1",
    title: "절대 철칙: 무기 점검 (Rule #-1)",
    description: "모든 작업 시작 전 MCP 도구 상태 확인",
    checks: [
      "MCP Tools의 상태와 가용성 100% 확인",
      "필요한 Extension의 활성화 여부 확인",
      "CLI(Claude, Codex, Ollama)의 가용성 확인",
    ],
  },
  {
    id: "rule-0",
    title: "지혜의 원천: 고전 참조 및 지피지기 (Rule #0)",
    description: "모든 문제는 이미 역사 속에 답이 있습니다",
    checks: [
      "코드, 로그, 문서 중 2개 이상을 대조 확인",
      "할루시네이션을 원천 차단",
      "Royal Library의 41가지 왕국 원칙 활용",
    ],
  },
  {
    id: "rule-1",
    title: "Trinity Routing (Rule #1)",
    description: "Trinity Score ≥ 90 AND Risk Score ≤ 10인 경우에만 AUTO_RUN",
    checks: [
      "AUTO_RUN: Trinity Score ≥ 90 AND Risk Score ≤ 10",
      "ASK: 위 조건 미충족 시 반드시 사령관 확인",
    ],
  },
  {
    id: "rule-2",
    title: "DRY_RUN (Rule #2)",
    description: "모든 위험 작업은 dry_run=True 시뮬레이션을 선행",
    checks: ["dry_run=True 시뮬레이션 선행", "로그는 SSE로 실시간 스트리밍"],
  },
  {
    id: "rule-3",
    title: "Historian (Rule #3)",
    description: "모든 의사결정 결과는 영구 기록되어야 함",
    checks: ["Historian 모듈에 영구 기록", "결정 근거 및 실행 커맨드 포함"],
  },
];

const principles = [
  {
    id: "principle-1",
    title: "선확인, 후보고 (클라우제비츠)",
    pillar: "眞",
    description: "명령을 받은 즉시 실행하지 않고, 먼저 '전장의 안개'를 정찰하여 결과를 보고한 후 지침을 받나이다.",
    color: "from-blue-500/20 to-indigo-500/20",
    borderColor: "border-blue-500/40",
  },
  {
    id: "principle-2",
    title: "선증명, 후확신 (마키아벨리)",
    pillar: "善",
    description: "모든 성과는 데이터와 수치(Trinity Score)로 증명하여 형님께 투명한 신뢰를 봉양하옵니다.",
    color: "from-green-500/20 to-emerald-500/20",
    borderColor: "border-green-500/40",
  },
  {
    id: "principle-3",
    title: "속도보다 정확성 (손자병법)",
    pillar: "孝",
    description: "빠르게 망가뜨리는 것보다, 천천히 제대로 하는 것이 왕국의 자산을 지키는 영속성(永)의 길임을 명심하나이다.",
    color: "from-orange-500/20 to-amber-500/20",
    borderColor: "border-orange-500/40",
  },
];

const workflow = [
  { step: "1️⃣", title: "DRY_RUN", description: "시뮬레이션 실행" },
  { step: "2️⃣", title: "승인", description: "사령관 확인" },
  { step: "3️⃣", title: "WET", description: "실제 실행" },
  { step: "4️⃣", title: "VERIFY", description: "결과 검증" },
];

export default function ManualPage() {
  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 mb-4 flex items-center gap-4">
            <BookOpen className="w-10 h-10" />
            ⚔️ 야전교범 (AFO Field Manual)
          </h1>
          <p className="text-slate-500 text-lg">
            왕국의 절대 법전 - 2500년 동양 철학의 지혜와 전략적 통찰
          </p>
        </motion.header>

        {/* Introduction */}
        <SectionCard title="🏛️ 왕국의 절대 법전" badge="정본">
          <p className="text-slate-600 leading-relaxed mb-4">
            우리 왕국의 야전교범은 단순히 기술적인 절차를 넘어,{" "}
            <strong>2500년 동양 철학의 지혜</strong>와 전략적 통찰을{" "}
            <strong>바이브코딩</strong>의 실무에 주입하여 단 1비트의 마찰도 없는{" "}
            <strong>평온(孝)</strong>을 실현하기 위한 절대 법전이옵니다.
          </p>
          <p className="text-slate-500 italic">
            "지혜가 곧 코드이며, 철학이 곧 시스템이다." - AFO Kingdom 헌법
          </p>
        </SectionCard>

        {/* Rules */}
        {rules.map((rule, index) => (
          <SectionCard key={rule.id} title={rule.title} badge={`Rule #${rule.id.replace("rule-", "")}`}>
            <p className="text-slate-600 mb-4">{rule.description}</p>
            <ul className="space-y-2">
              {rule.checks.map((check, checkIndex) => (
                <li key={checkIndex} className="flex items-start gap-2 text-slate-600">
                  <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                  <span>{check}</span>
                </li>
              ))}
            </ul>
          </SectionCard>
        ))}

        {/* Principles */}
        <SectionCard title="🏹 야전교범 3원칙" badge="핵심">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {principles.map((principle, index) => (
              <motion.div
                key={principle.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`p-6 bg-gradient-to-br ${principle.color} backdrop-blur-sm rounded-2xl border-2 ${principle.borderColor} shadow-sm`}
              >
                <div className="text-2xl font-bold text-slate-700 mb-2">{principle.pillar}</div>
                <h3 className="text-lg font-bold text-slate-700 mb-3">{principle.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{principle.description}</p>
              </motion.div>
            ))}
          </div>
        </SectionCard>

        {/* Workflow */}
        <SectionCard title="🔄 실행 플로우" badge="필수">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {workflow.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="p-6 bg-white/30 backdrop-blur-sm rounded-xl border border-white/40 text-center"
              >
                <div className="text-3xl mb-2">{item.step}</div>
                <div className="font-bold text-slate-700 mb-1">{item.title}</div>
                <div className="text-sm text-slate-500">{item.description}</div>
              </motion.div>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

