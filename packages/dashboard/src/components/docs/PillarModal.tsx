'use client';

import { useMemo } from 'react';
import { Modal } from './Modal';

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
  isOpen: boolean;
  onClose: () => void;
  pillarName: string;
}

const pillarData: Record<string, PillarInfo> = {
  truth: {
    name: '眞',
    english: 'Truth',
    weight: 0.35,
    strategist: '제갈량 (Zhuge Liang)',
    symbol: '⚔️ 창',
    role: '기술적 확실성, 아키텍처·전략·개발 총괄',
    definition: '眞은 모든 것의 근본입니다.',
    tradition: '세종대왕의 한글 창제',
    implementation: '타입 안전성 준수',
    philosophy: '실제 데이터만 사용',
    documentation: '眞은 기술적 확실성을 의미합니다.',
  },
  goodness: {
    name: '善',
    english: 'Goodness',
    weight: 0.35,
    strategist: '사마의 (Sima Yi)',
    symbol: '🛡️ 방패',
    role: '윤리·안정·통합',
    definition: '善은 윤리적 행위를 의미합니다.',
    tradition: '홍익인간',
    implementation: 'Constitutional AI',
    philosophy: '사령관의 평온 최우선',
    documentation: '善은 윤리적 안정성을 의미합니다.',
  },
  beauty: {
    name: '美',
    english: 'Beauty',
    weight: 0.2,
    strategist: '주유 (Zhou Yu)',
    symbol: '🌉 다리',
    role: '서사·UX',
    definition: '美는 단순함과 우아함입니다.',
    tradition: '중용',
    implementation: 'Framer Motion 애니메이션',
    philosophy: '인지 부하 최소화',
    documentation: '美는 구조적 우아함을 의미합니다.',
  },
  serenity: {
    name: '孝',
    english: 'Serenity',
    weight: 0.08,
    guardian: '승상 (Chancellor)',
    symbol: '🕊️ 평온',
    role: '평온 수호',
    definition: '孝는 사령관의 평온을 수호합니다.',
    tradition: '효의 전통',
    implementation: '실시간 하트비트',
    philosophy: '마찰 원천 차단',
    documentation: '孝는 평온과 마찰 제거를 의미합니다.',
  },
  eternity: {
    name: '永',
    english: 'Eternity',
    weight: 0.02,
    guardian: '승상 (Chancellor)',
    symbol: '♾️ 영원',
    role: '영속성',
    definition: '永는 영속적 계승을 의미합니다.',
    tradition: '영원한 기록',
    implementation: 'Redis Saver',
    philosophy: '지식의 영속적 계승',
    documentation: '永는 영속적 계승을 의미합니다.',
  },
};

export function PillarModal({
  isOpen,
  onClose,
  pillarName,
}: PillarModalProps) {
  const pillar = useMemo(() => {
    return (pillarName && pillarData[pillarName]) || null;
  }, [pillarName]);

  if (!pillar) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`${pillar.symbol} ${pillar.name} (${pillar.english})`}
      size='lg'
    >
      <div className='space-y-6'>
        <div className='grid grid-cols-2 gap-4'>
          <div className='p-4 bg-slate-50 rounded-lg'>
            <div className='text-sm text-slate-500 mb-1'>가중치</div>
            <div className='text-2xl font-bold text-slate-700'>
              {(pillar.weight * 100).toFixed(0)}%
            </div>
          </div>
          <div className='p-4 bg-slate-50 rounded-lg'>
            <div className='text-sm text-slate-500 mb-1'>담당자</div>
            <div className='text-lg font-semibold text-slate-700'>
              {pillar.strategist || pillar.guardian}
            </div>
          </div>
        </div>
        <div>
          <h3 className='text-lg font-bold text-slate-700 mb-2'>역할</h3>
          <p className='text-slate-600'>{pillar.role}</p>
        </div>
        <div>
          <h3 className='text-lg font-bold text-slate-700 mb-2'>정의</h3>
          <p className='text-slate-600 leading-relaxed'>{pillar.definition}</p>
        </div>
      </div>
    </Modal>
  );
}
