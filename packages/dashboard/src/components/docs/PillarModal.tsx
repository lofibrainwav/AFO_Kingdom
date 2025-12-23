"use client";

import { useState, useEffect } from "react";
import { Modal } from "./Modal";
import { motion } from "framer-motion";

interface PillarInfo {
  name: string;
  english: string;
  weight: number;
  strategist?: string;
  guardian?: string;
  symbol: string;
  role: string;
  definition: string;
  tradition: string;
  implementation: string;
  philosophy: string;
  documentation: string;
}

interface PillarModalProps {
  /**
   * 모달 표시 여부
   */
  isOpen: boolean;
  /**
   * 모달 닫기 함수
   */
  onClose: () => void;
  /**
   * 기둥 이름 (truth, goodness, beauty, serenity, eternity)
   */
  pillarName: string;
}

const pillarData: Record<string, PillarInfo> = {
  truth: {
    name: "眞",
    english: "Truth",
    weight: 0.35,
    strategist: "제갈량 (Zhuge Liang)",
    symbol: "⚔️ 창",
    role: "기술적 확실성, 아키텍처·전략·개발 총괄",
    definition:
      "眞은 모든 것의 근본입니다. 거짓 위에 세워진 것은 결국 무너집니다. 기술적 확실성과 사실 기반 의사결정이 핵심입니다.",
    tradition:
      "세종대왕의 한글 창제, 지피지기(知彼知己) 원칙, 사실 기반 의사결정의 전통을 이어받습니다.",
    implementation:
      "모든 데이터는 최소 2개 출처로 검증되며, 타입 안전성(MyPy strict), CI/CD LOCK 원칙을 준수합니다.",
    philosophy:
      "Rule #0: 모르면 움직이지 않는다. NO MOCK, 실제 데이터만 사용. 기술적 확실성이 모든 결정의 기반입니다.",
    documentation:
      "眞은 기술적 확실성을 의미하며, 모든 시스템의 근본이 되는 원칙입니다. 타입 안전성, 사실 검증, 아키텍처 설계가 핵심입니다.",
  },
  goodness: {
    name: "善",
    english: "Goodness",
    weight: 0.35,
    strategist: "사마의 (Sima Yi)",
    symbol: "🛡️ 방패",
    role: "윤리·안정·통합·게이트키퍼",
    definition:
      "善은 윤리적 행위와 인간 중심성을 의미합니다. 기술은 사람을 위한 도구일 뿐입니다.",
    tradition:
      "홍익인간(弘益人間), 측은지심(惻隱之心), 공정과 정의의 전통을 이어받습니다.",
    implementation:
      "모든 행동은 인간에게 이로운지 Trinity Score로 평가되며, Constitutional AI 엔진으로 윤리적 검증을 수행합니다.",
    philosophy:
      "인간 중심 설계, 윤리적 자동화, 해악을 끼치지 않는 시스템. 사령관의 평온(Serenity)을 최우선으로 고려합니다.",
    documentation:
      "善은 윤리적 안정성과 리스크 관리를 의미합니다. AUTO_RUN 게이트, DRY_RUN 기본값, CAI 엔진이 핵심입니다.",
  },
  beauty: {
    name: "美",
    english: "Beauty",
    weight: 0.2,
    strategist: "주유 (Zhou Yu)",
    symbol: "🌉 다리",
    role: "서사·UX·취향정렬·인지부하 제거",
    definition:
      "美는 단순함과 우아함, 조화로움입니다. 복잡함을 아름답게 녹입니다.",
    tradition:
      "중용(中庸), 예술과 문화의 아름다움, 자연의 조화의 전통을 이어받습니다.",
    implementation:
      "4계층 아키텍처(Presentation → Application → Domain → Infrastructure), Glassmorphism UX, 일관된 네이밍 컨벤션을 적용합니다.",
    philosophy:
      "응집도는 높고 결합도는 낮은 우아함. 사용자 경험 최적화, 인지 부하 최소화. 코드가 한 편의 시와 같은 질서를 갖춥니다.",
    documentation:
      "美는 구조적 우아함과 미학적 정합성을 의미합니다. 아키텍처 설계, UX 디자인, 네이밍 컨벤션이 핵심입니다.",
  },
  serenity: {
    name: "孝",
    english: "Serenity",
    weight: 0.08,
    guardian: "승상 (Chancellor)",
    symbol: "🕊️ 평온",
    role: "사령관 평온 수호, 마찰(Friction) 제거",
    definition:
      "孝는 사령관의 평온을 수호하고 시스템의 마찰을 제거하는 것입니다.",
    tradition: "효(孝)의 전통 - 상위자의 평온을 최우선으로 보호하는 마음",
    implementation:
      "Rule #-1 무기 점검(MCP 도구 상태 확인), 11-오장육부 건강 진단, SSE 로그 스트리밍을 통한 실시간 투명성 제공.",
    philosophy:
      "사령관의 평온이 곧 시스템의 안정성. 모든 마찰(Friction)을 원천 차단. AntiGravity 시스템으로 자동화를 통한 평온 확보.",
    documentation:
      "孝는 사령관의 평온과 마찰 제거를 의미합니다. MCP 도구 점검, 오장육부 건강 모니터링, 실시간 투명성이 핵심입니다.",
  },
  eternity: {
    name: "永",
    english: "Eternity",
    weight: 0.02,
    guardian: "승상 (Chancellor)",
    symbol: "♾️ 영원",
    role: "영속성·레거시 유지, 장기적 지속가능성",
    definition:
      "永는 영속적 계승과 자율 진화를 의미합니다. 시스템이 영원히 지속되도록 합니다.",
    tradition: "영원한 기억, 역사적 기록, 지식의 계승 전통",
    implementation:
      "AsyncRedisSaver와 Redis Checkpoint를 통한 영구 컨텍스트 보존, Project Genesis(자기 확장 모드), 풍부한 Markdown 문서화.",
    philosophy:
      "모든 설계 의도와 히스토리가 영구히 보존됩니다. 시스템이 스스로 진화하며 영토를 넓혀갑니다. 문서화를 통한 지식의 영속적 계승.",
    documentation:
      "永는 영속적 계승과 자율 진화를 의미합니다. 영구 컨텍스트 보존, 자기 확장 모드, 풍부한 문서화가 핵심입니다.",
  },
};

/**
 * 진선미효영 기둥 상세 모달
 * 
 * @example
 * ```tsx
 * <PillarModal
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   pillarName="truth"
 * />
 * ```
 */
export function PillarModal({
  isOpen,
  onClose,
  pillarName,
}: PillarModalProps) {
  const [pillar, setPillar] = useState<PillarInfo | null>(null);

  useEffect(() => {
    if (pillarName && pillarData[pillarName]) {
      setPillar(pillarData[pillarName]);
    }
  }, [pillarName]);

  if (!pillar) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`${pillar.symbol} ${pillar.name} (${pillar.english})`}
      size="lg"
    >
      <div className="space-y-6">
        {/* Header Info */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-slate-50 rounded-lg">
            <div className="text-sm text-slate-500 mb-1">가중치</div>
            <div className="text-2xl font-bold text-slate-700">
              {(pillar.weight * 100).toFixed(0)}%
            </div>
          </div>
          <div className="p-4 bg-slate-50 rounded-lg">
            <div className="text-sm text-slate-500 mb-1">담당자</div>
            <div className="text-lg font-semibold text-slate-700">
              {pillar.strategist || pillar.guardian}
            </div>
          </div>
        </div>

        {/* Role */}
        <div>
          <h3 className="text-lg font-bold text-slate-700 mb-2">역할</h3>
          <p className="text-slate-600">{pillar.role}</p>
        </div>

        {/* Definition */}
        <div>
          <h3 className="text-lg font-bold text-slate-700 mb-2">정의</h3>
          <p className="text-slate-600 leading-relaxed">{pillar.definition}</p>
        </div>

        {/* Tradition */}
        <div>
          <h3 className="text-lg font-bold text-slate-700 mb-2">전통</h3>
          <p className="text-slate-600 leading-relaxed">{pillar.tradition}</p>
        </div>

        {/* Implementation */}
        <div>
          <h3 className="text-lg font-bold text-slate-700 mb-2">구현</h3>
          <p className="text-slate-600 leading-relaxed">
            {pillar.implementation}
          </p>
        </div>

        {/* Philosophy */}
        <div>
          <h3 className="text-lg font-bold text-slate-700 mb-2">철학</h3>
          <p className="text-slate-600 leading-relaxed">{pillar.philosophy}</p>
        </div>

        {/* Documentation */}
        <div>
          <h3 className="text-lg font-bold text-slate-700 mb-2">문서화</h3>
          <p className="text-slate-600 leading-relaxed">
            {pillar.documentation}
          </p>
        </div>
      </div>
    </Modal>
  );
}

