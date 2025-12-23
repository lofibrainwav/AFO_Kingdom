"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { BookOpen, GitBranch, FolderTree, Network, Sparkles, Activity, Users, FileText, Wrench, Heart, BookMarked } from "lucide-react";

const docSections = [
  {
    id: "philosophy",
    title: "眞善美孝永 - 왕국의 철학",
    description: "5기둥 철학과 Trinity Score 계산",
    icon: Sparkles,
    href: "/docs/philosophy",
    gradient: "from-purple-500/20 to-indigo-500/20",
  },
  {
    id: "realtime-status",
    title: "실시간 상태 대시보드",
    description: "Git 상태, 구현 진행률, 시스템 부하 모니터링",
    icon: Activity,
    href: "/docs/realtime-status",
    gradient: "from-blue-500/20 to-cyan-500/20",
  },
  {
    id: "chancellor",
    title: "승상 시스템",
    description: "3책사 병렬 조율과 5호대장군 실행 구조",
    icon: Users,
    href: "/docs/chancellor",
    gradient: "from-indigo-500/20 to-purple-500/20",
  },
  {
    id: "ssot",
    title: "SSOT",
    description: "Single Source of Truth - 페르소나/명칭 정본",
    icon: FileText,
    href: "/docs/ssot",
    gradient: "from-emerald-500/20 to-teal-500/20",
  },
  {
    id: "git-tree",
    title: "Git 트리 분석",
    description: "Phase별 진화 과정과 커밋 히스토리",
    icon: GitBranch,
    href: "/docs/git-tree",
    gradient: "from-blue-500/20 to-cyan-500/20",
  },
  {
    id: "project-structure",
    title: "프로젝트 구조",
    description: "패키지별 상세 분석과 디렉토리 트리",
    icon: FolderTree,
    href: "/docs/project-structure",
    gradient: "from-green-500/20 to-emerald-500/20",
  },
  {
    id: "architecture",
    title: "시스템 아키텍처",
    description: "4계층 아키텍처와 데이터 플로우",
    icon: Network,
    href: "/docs/architecture",
    gradient: "from-orange-500/20 to-red-500/20",
  },
  {
    id: "organs-map",
    title: "오장육부 지도",
    description: "11-Organ System 기술 매핑",
    icon: Heart,
    href: "/docs/organs-map",
    gradient: "from-pink-500/20 to-rose-500/20",
  },
  {
    id: "mcp-tools",
    title: "MCP 도구",
    description: "Model Context Protocol 도구 관리",
    icon: Wrench,
    href: "/docs/mcp-tools",
    gradient: "from-cyan-500/20 to-blue-500/20",
  },
  {
    id: "tools",
    title: "Skills & 도구",
    description: "19개 스킬 레지스트리",
    icon: Wrench,
    href: "/docs/tools",
    gradient: "from-violet-500/20 to-purple-500/20",
  },
  {
    id: "manual",
    title: "야전교범",
    description: "AFO Field Manual - 절대 법전",
    icon: BookMarked,
    href: "/docs/manual",
    gradient: "from-amber-500/20 to-orange-500/20",
  },
  {
    id: "agents-md",
    title: "AGENTS.md",
    description: "모든 AI 코딩 에이전트 공용 지침서",
    icon: FileText,
    href: "/docs/agents-md",
    gradient: "from-slate-500/20 to-gray-500/20",
  },
  {
    id: "claude-md",
    title: "CLAUDE.md",
    description: "Claude 에이전트 전용 지침서",
    icon: FileText,
    href: "/docs/claude-md",
    gradient: "from-amber-500/20 to-yellow-500/20",
  },
  {
    id: "codex-md",
    title: "CODEX.md",
    description: "OpenAI Codex 에이전트 전용 지침서",
    icon: FileText,
    href: "/docs/codex-md",
    gradient: "from-green-500/20 to-emerald-500/20",
  },
  {
    id: "cursor-md",
    title: "CURSOR.md",
    description: "Cursor IDE 에이전트 전용 지침서",
    icon: FileText,
    href: "/docs/cursor-md",
    gradient: "from-blue-500/20 to-cyan-500/20",
  },
  {
    id: "grok-md",
    title: "GROK.md",
    description: "xAI Grok 에이전트 전용 지침서",
    icon: FileText,
    href: "/docs/grok-md",
    gradient: "from-purple-500/20 to-pink-500/20",
  },
];

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="flex items-center gap-4 mb-4">
            <BookOpen className="w-10 h-10 text-slate-600" />
            <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400">
              📐 AFO Kingdom - 설계도 & 문서
            </h1>
          </div>
          <p className="text-slate-500 text-lg">眞善美孝永 5기둥 철학 기반 통합 AI 운영 체제</p>
        </motion.header>

        {/* Section Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {docSections.map((section, index) => {
            const Icon = section.icon;
            return (
              <motion.div
                key={section.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Link href={section.href}>
                  <div
                    className={`bg-gradient-to-br ${section.gradient} backdrop-blur-sm rounded-3xl p-8 border border-white/40 shadow-inner hover:shadow-xl transition-all cursor-pointer group h-full`}
                  >
                    <div className="flex items-start gap-4 mb-4">
                      <div className="p-3 bg-white/20 rounded-xl group-hover:scale-110 transition-transform">
                        <Icon className="w-8 h-8 text-slate-700" />
                      </div>
                      <div className="flex-1">
                        <h2 className="text-2xl font-bold text-slate-700 mb-2">{section.title}</h2>
                        <p className="text-slate-500 text-sm">{section.description}</p>
                      </div>
                    </div>
                    <div className="mt-4 flex items-center text-slate-600 text-sm font-medium group-hover:translate-x-2 transition-transform">
                      자세히 보기 →
                    </div>
                  </div>
                </Link>
              </motion.div>
            );
          })}
        </div>

        {/* Quick Links */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 p-6 bg-white/30 backdrop-blur-sm rounded-2xl border border-white/40"
        >
          <h3 className="text-xl font-bold text-slate-700 mb-4">빠른 링크</h3>
          <div className="flex flex-wrap gap-4">
            <Link
              href="/"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              메인 대시보드
            </Link>
            <Link
              href="/git-tree"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              Git 트리 (기존)
            </Link>
            <Link
              href="/kingdom-status"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              Kingdom Status
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
