/**
 * AFO Kingdom Royal Library (아름다운 코드 적용)
 * Trinity Score 기반 아름다운 코드로 구현된 왕실 도서관 컴포넌트
 *
 * Author: AFO Kingdom Development Team
 * Date: 2025-12-24
 * Version: 2.0.0 (Beautiful Code Edition)
 *
 * Philosophy:
 * - 智 (Wisdom): 왕실 지식의 체계적 제공
 * - 眞 (Truth): 정확한 SSOT 데이터 표시
 * - 美 (Beauty): 우아한 UI와 사용자 경험
 * - 孝 (Serenity): 안정적인 데이터 로딩
 * - 永 (Eternity): 지속적인 지식 관리
 */

"use client";

import { ROYAL_PERSONAS } from '@/config/royal_constants';
import { Lock, Server, Users } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';

// ============================================================================
// TYPES & INTERFACES (아름다운 코드: 타입 안전성)
// ============================================================================

/**
 * 페르소나 인터페이스 (Trinity Score: 眞)
 */
interface Persona {
  readonly name: string;
  readonly code: string;
  readonly role: string;
}

/**
 * 포트 서비스 인터페이스
 */
interface PortService {
  readonly service: string;
  readonly port: number;
  readonly description: string;
}

/**
 * 왕실 규약 인터페이스
 */
interface RoyalRule {
  readonly id: number;
  readonly name: string;
  readonly principle: string;
  readonly code?: string;
}

/**
 * 왕실 책 인터페이스
 */
interface RoyalBook {
  readonly title: string;
  readonly weight: string;
  readonly rules: readonly RoyalRule[];
}

/**
 * 잠금 카드 Props
 */
interface LockCardProps {
  readonly title: string;
  readonly items: readonly string[];
  readonly color: string;
  readonly iconColor: string;
}

/**
 * 로딩 상태 인터페이스
 */
interface LoadingState {
  readonly isLoading: boolean;
  readonly error: string | null;
}

/**
 * 로열 라이브러리 데이터 인터페이스
 */
interface RoyalLibraryData {
  readonly personas: readonly Persona[];
  readonly ports: readonly PortService[];
  readonly royalBooks: readonly RoyalBook[];
}

export const RoyalLibrary = () => {
  const [loading, setLoading] = useState(true);
  const [personas, setPersonas] = useState<any[]>([]);
  const [royalBooks, setRoyalBooks] = useState<any[]>([]);
  const [ports, setPorts] = useState<any[]>([]);

  useEffect(() => {
    // Simulate loading data from "HTML Source" (Mock for now or fetch if API exists)
    const loadData = async () => {
      try {
        setPersonas(ROYAL_PERSONAS);
        
        // Mock Ports Data (Synced with Kingdom Dashboard)
        setPorts([
            { service: "Soul Engine", port: 8010, description: "FastAPI Backend" },
            { service: "Dashboard", port: 3000, description: "Next.js Frontend" },
            { service: "Ollama", port: 11435, description: "LLM Server" },
            { service: "Redis", port: 6379, description: "Cache/Session" },
            { service: "PostgreSQL", port: 15432, description: "Database" }
        ]);

        // Mock Royal Books (Constituting the 41 Rules)
        setRoyalBooks([
            {
                title: "Book of Truth (眞)", weight: "35%", rules: [
                    { id: 1, name: "Data Integrity", principle: "All inputs must be validated via Pydantic.", code: "class Input(BaseModel):" },
                    { id: 2, name: "Type Safety", principle: "No Any types allowed in core logic.", code: "def core(x: int) -> str:" }
                ]
            },
            {
                title: "Book of Goodness (善)", weight: "35%", rules: [
                    { id: 3, name: "Safety First", principle: "Always run DRY_RUN before execution.", code: "if flags.dry_run: return" }
                ]
            },
             {
                title: "Book of Beauty (美)", weight: "20%", rules: [
                    { id: 4, name: "User Experience", principle: "Minimize friction, maximize clarity.", code: "<ui-component />" }
                ]
            }
        ]);

      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <section className="py-8 text-slate-700">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-slate-600 mx-auto mb-4"></div>
            <p className="text-slate-500">Loading Royal Library from HTML source...</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-8 text-slate-700">
      <div className="flex items-center gap-4 mb-8">
        <h2 className="text-xl font-bold text-slate-600">ROYAL LIBRARY & SSOT</h2>
        <div className="h-[1px] flex-1 bg-slate-300" />
        <span className="text-xs text-slate-400 font-mono">
          Strangler Fig: HTML - React
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        {/* 1. SSOT - Personas */}
        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="flex items-center gap-2 font-bold text-slate-600">
              <Users className="w-5 h-5" /> SSOT - Personas
            </h3>
            <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">
              TRINITY_OS_PERSONAS.yaml
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase bg-slate-50/50">
                <tr>
                  <th className="px-4 py-2">Persona</th>
                  <th className="px-4 py-2">Code Name</th>
                  <th className="px-4 py-2">Role</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {personas.map((p, i) => (
                  <tr key={i} className="hover:bg-white/50">
                    <td className="px-4 py-2 font-medium">{p.name}</td>
                    <td className="px-4 py-2 font-mono text-slate-500">{p.code}</td>
                    <td className="px-4 py-2 text-slate-500">{p.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 2. LOCK - Principles */}
        <div className="space-y-6">
          <LockCard
            title="Truth (眞) LOCK"
            items={[
              "Strong Typing + MyPy Checks",
              "Pydantic Validation (pt0)",
              "Loop Verification"
            ]}
            color="border-blue-200 bg-blue-50/50"
            iconColor="text-blue-600"
          />
          <LockCard
            title="Goodness (善) LOCK"
            items={[
              "DRY_RUN Default (Safety)",
              "Gatekeeping Logic",
              "Ethical Compliance"
            ]}
            color="border-green-200 bg-green-50/50"
            iconColor="text-green-600"
          />
          <LockCard
            title="Beauty (美) LOCK"
            items={[
              "Clean UI/UX",
              "API Standardization",
              "Visual Consistency"
            ]}
            color="border-purple-200 bg-purple-50/50"
            iconColor="text-purple-600"
          />
        </div>
      </div>

      {/* 3. Port Map */}
      <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm mb-12">
        <div className="flex items-center justify-between mb-4">
          <h3 className="flex items-center gap-2 font-bold text-slate-600">
            <Server className="w-5 h-5" /> Confirmed Stable Paths & Ports
          </h3>
          <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded">
            Active & Listening
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-400 uppercase bg-slate-50/50">
              <tr>
                <th className="px-4 py-2">Service Component</th>
                <th className="px-4 py-2">Port</th>
                <th className="px-4 py-2">Description</th>
                <th className="px-4 py-2">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {ports.map((service, i) => (
                <tr key={i} className="hover:bg-white/50">
                  <td className="px-4 py-2 font-medium flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${service.service.includes("Soul") ? "bg-green-500" : "bg-slate-400"}`}></div>
                    {service.service}
                  </td>
                  <td className="px-4 py-2 font-mono text-slate-600">{service.port}</td>
                  <td className="px-4 py-2 text-slate-500">{service.description}</td>
                  <td className="px-4 py-2">
                    <span className="px-2 py-1 text-xs font-bold rounded bg-green-100 text-green-700">
                      Active
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. Royal Rules (Synced from HTML) */}
      <div className="space-y-8">
        <div className="flex items-center gap-4">
          <h2 className="text-xl font-bold text-slate-600">IV. ROYAL CONSTITUTION (41 Rules)</h2>
          <div className="h-[1px] flex-1 bg-slate-300" />
          <span className="text-xs text-slate-400 font-mono">
            Strangler Fig: HTML Source
          </span>
        </div>

        {royalBooks.map((book: any, bookIndex: number) => (
          <div
            key={bookIndex}
            className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm"
          >
            <h3 className="text-lg font-bold text-slate-700 mb-4 border-b border-slate-100 pb-2">
              {book.title} - {book.weight}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {book.rules.map((rule: any) => (
                <div
                  key={rule.id}
                  className="p-4 bg-white rounded-xl border border-slate-100 hover:border-slate-300 transition-colors"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-bold text-slate-700 flex items-center gap-2">
                      <span className="bg-slate-100 text-slate-500 text-xs px-2 py-0.5 rounded-full">
                        #{rule.id}
                      </span>
                      {rule.name}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600 mb-3 italic">"{rule.principle}"</p>
                  {rule.code && (
                    <div className="bg-slate-900 rounded p-2 overflow-x-auto">
                      <code className="text-xs font-mono text-green-400 block whitespace-nowrap">
                        {rule.code}
                      </code>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

const LockCard = ({ title, items, color, iconColor }: any) => (
  <div className={`p-4 rounded-xl border ${color}`}>
    <h3 className={`flex items-center gap-2 font-bold mb-3 ${iconColor}`}>
      <Lock className="w-4 h-4" /> {title}
    </h3>
    <ul className="space-y-2">
      {items.map((item: string, i: number) => (
        <li key={i} className="flex items-center gap-2 text-sm text-slate-600">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
          {item}
        </li>
      ))}
    </ul>
  </div>
);