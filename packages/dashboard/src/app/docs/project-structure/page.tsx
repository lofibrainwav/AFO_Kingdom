'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Package, FileCode, Database, Layers } from 'lucide-react';

const packages = [
  {
    id: 'afo-core',
    name: 'afo-core',
    description: '백엔드 코어 (FastAPI, Python 3.12+)',
    icon: Database,
    stats: { python: 1506, files: 291 },
    color: 'from-blue-500/20 to-cyan-500/20',
  },
  {
    id: 'trinity-os',
    name: 'trinity-os',
    description: '오케스트레이션 계층 (MCP, Context7)',
    icon: Layers,
    stats: { python: 823, files: 156 },
    color: 'from-purple-500/20 to-pink-500/20',
  },
  {
    id: 'sixXon',
    name: 'sixXon',
    description: '6Xon 통합 모듈',
    icon: Package,
    stats: { python: 245, files: 45 },
    color: 'from-green-500/20 to-emerald-500/20',
  },
  {
    id: 'dashboard',
    name: 'dashboard',
    description: '프론트엔드 (Next.js 16, React 19)',
    icon: FileCode,
    stats: { typescript: 5439, files: 189 },
    color: 'from-orange-500/20 to-red-500/20',
  },
];

export default function ProjectStructurePage() {
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
                📦 프로젝트 구조
              </h1>
              <p className="text-slate-500 text-lg mt-2">
                패키지별 상세 분석과 디렉토리 트리
              </p>
            </div>
            <Link
              href="/docs"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              ← 문서 목록
            </Link>
          </div>
        </motion.header>

        {/* Overall Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12"
        >
          <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-6 border border-white/40">
            <div className="text-3xl font-bold text-slate-700 mb-2">1,506</div>
            <div className="text-slate-500 text-sm">Python 파일</div>
          </div>
          <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-6 border border-white/40">
            <div className="text-3xl font-bold text-slate-700 mb-2">5,439</div>
            <div className="text-slate-500 text-sm">TypeScript 파일</div>
          </div>
          <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-6 border border-white/40">
            <div className="text-3xl font-bold text-slate-700 mb-2">1,005</div>
            <div className="text-slate-500 text-sm">Markdown 문서</div>
          </div>
          <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-6 border border-white/40">
            <div className="text-3xl font-bold text-slate-700 mb-2">4</div>
            <div className="text-slate-500 text-sm">주요 패키지</div>
          </div>
        </motion.div>

        {/* Package Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {packages.map((pkg, index) => {
            const Icon = pkg.icon;
            return (
              <motion.div
                key={pkg.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
              >
                <div
                  className={`bg-gradient-to-br ${pkg.color} backdrop-blur-sm rounded-3xl p-8 border border-white/40 shadow-inner hover:shadow-xl transition-all h-full`}
                >
                  <div className="flex items-start gap-4 mb-4">
                    <div className="p-3 bg-white/20 rounded-xl">
                      <Icon className="w-8 h-8 text-slate-700" />
                    </div>
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold text-slate-700 mb-2">
                        {pkg.name}
                      </h2>
                      <p className="text-slate-500 text-sm">{pkg.description}</p>
                    </div>
                  </div>
                  <div className="mt-6 grid grid-cols-2 gap-4">
                    {Object.entries(pkg.stats).map(([key, value]) => (
                      <div key={key} className="bg-white/20 rounded-lg p-3">
                        <div className="text-2xl font-bold text-slate-700">{value}</div>
                        <div className="text-xs text-slate-500 uppercase">{key}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Directory Tree */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white/30 backdrop-blur-sm rounded-3xl p-8 border border-white/40"
        >
          <h2 className="text-2xl font-bold text-slate-700 mb-6">디렉토리 구조</h2>
          <pre className="text-sm text-slate-700 font-mono overflow-x-auto">
            {`AFO_Kingdom/
├── packages/
│   ├── afo-core/          # 백엔드 코어
│   │   ├── AFO/           # 도메인 로직
│   │   ├── api/           # FastAPI 라우터
│   │   └── services/      # 비즈니스 로직
│   ├── trinity-os/        # 오케스트레이션
│   │   └── trinity_os/    # MCP 서버
│   ├── sixXon/            # 6Xon 통합
│   └── dashboard/         # 프론트엔드
│       └── src/
│           ├── app/       # Next.js App Router
│           └── components/# React 컴포넌트
├── docs/                  # 문서
└── scripts/               # 유틸리티 스크립트`}
          </pre>
        </motion.div>

        {/* Links */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8 p-6 bg-white/30 backdrop-blur-sm rounded-2xl border border-white/40"
        >
          <h3 className="text-xl font-bold text-slate-700 mb-4">상세 문서</h3>
          <div className="flex flex-wrap gap-4">
            <a
              href="/docs/PROJECT_STRUCTURE_COMPLETE.md"
              target="_blank"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              전체 구조 문서
            </a>
            <a
              href="/docs/ARCHITECTURE_MAP.md"
              target="_blank"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              아키텍처 맵
            </a>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

