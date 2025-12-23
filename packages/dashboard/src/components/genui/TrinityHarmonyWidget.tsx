/**
 * TrinityHarmonyWidget - AFO 왕국의 Trinity Score 실시간 시각화 위젯
 *
 * 🎨 디자인 컨셉: 화타 VL 모델의 Vision/UX 전문성 반영
 * - 眞善美孝永 5기둥의 균형을 아름다운 시각화로 표현
 * - 실시간 Trinity Score 변동을 직관적으로 표시
 * - 왕국의 철학적 아름다움을 현대적인 UX로 구현
 */

'use client';

import { AnimatePresence, motion } from 'framer-motion';
import React, { useEffect, useState } from 'react';

interface PillarScore {
  truth: number;
  goodness: number;
  beauty: number;
  serenity: number;
  eternity: number;
}

interface TrinityHarmonyWidgetProps {
  className?: string;
  refreshInterval?: number;
}

const PILLAR_CONFIG = {
  truth: { name: '眞', color: '#FF6B6B', symbol: '⚖️', desc: '기술적 확실성' },
  goodness: { name: '善', color: '#4ECDC4', symbol: '🛡️', desc: '윤리적 안전성' },
  beauty: { name: '美', color: '#45B7D1', symbol: '🎨', desc: 'UX 아름다움' },
  serenity: { name: '孝', color: '#96CEB4', symbol: '🤝', desc: '마찰 감소' },
  eternity: { name: '永', color: '#FECA57', symbol: '🔮', desc: '지속 가능성' }
};

export const TrinityHarmonyWidget: React.FC<TrinityHarmonyWidgetProps> = ({
  className = '',
  refreshInterval = 5000
}) => {
  const [scores, setScores] = useState<PillarScore>({
    truth: 85,
    goodness: 92,
    beauty: 78,
    serenity: 88,
    eternity: 76
  });

  const [isLoading, setIsLoading] = useState(false);

  // 실시간 Trinity Score 시뮬레이션
  useEffect(() => {
    const updateScores = () => {
      setScores(prev => ({
        truth: Math.max(0, Math.min(100, prev.truth + (Math.random() - 0.5) * 10)),
        goodness: Math.max(0, Math.min(100, prev.goodness + (Math.random() - 0.5) * 8)),
        beauty: Math.max(0, Math.min(100, prev.beauty + (Math.random() - 0.5) * 12)),
        serenity: Math.max(0, Math.min(100, prev.serenity + (Math.random() - 0.5) * 6)),
        eternity: Math.max(0, Math.min(100, prev.eternity + (Math.random() - 0.5) * 4))
      }));
    };

    const interval = setInterval(updateScores, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  // 조화도 계산 (Trinity Score 공식 적용)
  const harmonyLevel = React.useMemo(() => {
    const weights = { truth: 0.35, goodness: 0.35, beauty: 0.20, serenity: 0.08, eternity: 0.02 };
    const totalScore = Object.entries(scores).reduce((sum, [key, value]) => {
      return sum + (value * weights[key as keyof PillarScore]);
    }, 0);

    return Math.round(totalScore);
  }, [scores]);

  const getHarmonyColor = (level: number) => {
    if (level >= 90) return '#10B981'; // 초록 - 완벽한 조화
    if (level >= 80) return '#3B82F6'; // 파랑 - 좋은 조화
    if (level >= 70) return '#F59E0B'; // 노랑 - 보통 조화
    return '#EF4444'; // 빨강 - 불균형
  };

  const getHarmonyStatus = (level: number) => {
    if (level >= 90) return '완벽한 조화 ✨';
    if (level >= 80) return '균형 잡힘 🌊';
    if (level >= 70) return '안정적 ⚖️';
    return '조정 필요 🔧';
  };

  return (
    <motion.div
      className={`bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-2xl p-6 border border-purple-500/20 ${className}`}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            🌟 Trinity Harmony
          </h3>
          <p className="text-sm text-slate-400 mt-1">AFO 왕국의 5기둥 균형 상태</p>
        </div>

        {/* 조화도 표시 */}
        <motion.div
          className="text-right"
          animate={{ scale: harmonyLevel >= 90 ? [1, 1.1, 1] : 1 }}
          transition={{ duration: 2, repeat: harmonyLevel >= 90 ? Infinity : 0 }}
        >
          <div className="text-3xl font-bold" style={{ color: getHarmonyColor(harmonyLevel) }}>
            {harmonyLevel}
          </div>
          <div className="text-xs text-slate-400">
            {getHarmonyStatus(harmonyLevel)}
          </div>
        </motion.div>
      </div>

      {/* 5기둥 시각화 */}
      <div className="space-y-4">
        {Object.entries(scores).map(([key, score], index) => {
          const config = PILLAR_CONFIG[key as keyof typeof PILLAR_CONFIG];

          return (
            <motion.div
              key={key}
              className="flex items-center space-x-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              {/* 심볼 */}
              <div className="w-10 h-10 rounded-full flex items-center justify-center text-lg"
                   style={{ backgroundColor: config.color + '20', color: config.color }}>
                {config.symbol}
              </div>

              {/* 정보 */}
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-white">
                    {config.name} {config.desc}
                  </span>
                  <span className="text-sm font-bold" style={{ color: config.color }}>
                    {Math.round(score)}
                  </span>
                </div>

                {/* 프로그레스 바 */}
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <motion.div
                    className="h-2 rounded-full"
                    style={{ backgroundColor: config.color }}
                    initial={{ width: 0 }}
                    animate={{ width: `${score}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                  />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* 중앙 조화 코어 */}
      <div className="mt-8 flex justify-center">
        <motion.div
          className="relative w-24 h-24 rounded-full flex items-center justify-center border-4"
          style={{ borderColor: getHarmonyColor(harmonyLevel) + '50' }}
          animate={{
            boxShadow: harmonyLevel >= 90
              ? [`0 0 20px ${getHarmonyColor(harmonyLevel)}`, `0 0 40px ${getHarmonyColor(harmonyLevel)}`, `0 0 20px ${getHarmonyColor(harmonyLevel)}`]
              : `0 0 10px ${getHarmonyColor(harmonyLevel)}`
          }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="text-2xl">⚖️</div>
          <AnimatePresence>
            {harmonyLevel >= 90 && (
              <motion.div
                className="absolute inset-0 rounded-full border-2 border-yellow-400"
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1.2, opacity: [0, 1, 0] }}
                exit={{ scale: 0, opacity: 0 }}
                transition={{ duration: 3, repeat: Infinity }}
              />
            )}
          </AnimatePresence>
        </motion.div>
      </div>

      {/* 푸터 메시지 */}
      <motion.div
        className="mt-6 text-center text-xs text-slate-400"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
      >
        <p>眞善美孝永 - 왕국의 균형이 곧 힘입니다</p>
        <p className="mt-1 text-slate-500">실시간 업데이트 • 화타 VL 모델 디자인</p>
      </motion.div>
    </motion.div>
  );
};

export default TrinityHarmonyWidget;
