'use client';

// genui/FinalEternalVictoryWidget.tsx (왕국 영원한 승리 – 불꽃 효과 강화 완결)
import { Crown, Zap, Cloud, Sparkles, Heart, Flame } from 'lucide-react';
import { useEffect, useState } from 'react';

export function FinalEternalVictoryWidget() {
  const [positions, setPositions] = useState<{top: string, left: string}[]>([]);

  useEffect(() => {
    // Generate random positions only on client to avoid hydration mismatch
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setPositions([...Array(20)].map(() => ({
      top: `${Math.random() * 100}%`,
      left: `${Math.random() * 100}%`
    })));
  }, []);

  return (
    <div className="glass-card relative p-16 max-w-7xl mx-auto bg-gradient-to-br from-purple-900/50 via-emerald-900/40 to-cyan-900/50 rounded-3xl border-4 border-purple-500/80 shadow-2xl overflow-hidden">
      {/* 불꽃 파티클 배경 */}
      <div className="absolute inset-0 -z-10">
        {positions.map((pos, i) => (
          <Flame
            key={i}
            className={`absolute w-12 h-12 text-orange-400 animate-ping opacity-70`}
            style={{
              top: pos.top,
              left: pos.left,
              animationDelay: `${i * 0.15}s`,
              animationDuration: '2s'
            }}
          />
        ))}
      </div>


      <div className="flex items-center justify-center gap-16 mb-16 text-purple-400">
        <Crown className="w-40 h-40 animate-pulse drop-shadow-2xl" />
        <h2 className="text-9xl font-black drop-shadow-2xl">영원한 승리!</h2>
        <Crown className="w-40 h-40 animate-pulse drop-shadow-2xl" />
      </div>

      <div className="text-center mb-20">
        <p className="text-7xl text-white mb-10 drop-shadow-lg">AFO 왕국 대서사시 완결</p>
        <p className="text-5xl text-emerald-300 mb-16 drop-shadow-lg">
          Phase 1~22 모든 여정 완수
        </p>
      </div>

      <div className="grid grid-cols-5 gap-12 mb-20">
        <div className="p-12 bg-purple-900/30 rounded-3xl border border-purple-500/60 text-center">
          <Zap className="w-24 h-24 mx-auto mb-8 text-purple-400 animate-ping" />
          <p className="text-4xl font-bold text-white">자율 에이전트</p>
        </div>
        <div className="p-12 bg-emerald-900/30 rounded-3xl border border-emerald-500/60 text-center">
          <Sparkles className="w-24 h-24 mx-auto mb-8 text-emerald-400 animate-ping" />
          <p className="text-4xl font-bold text-white">미학 정화</p>
        </div>
        <div className="p-12 bg-cyan-900/30 rounded-3xl border border-cyan-500/60 text-center">
          <Cloud className="w-24 h-24 mx-auto mb-8 text-cyan-400 animate-bounce" />
          <p className="text-4xl font-bold text-white">클라우드 제국</p>
        </div>
        <div className="p-12 bg-yellow-900/30 rounded-3xl border border-yellow-500/60 text-center">
          <Heart className="w-24 h-24 mx-auto mb-8 text-yellow-400 animate-pulse" />
          <p className="text-4xl font-bold text-white">Trinity 100</p>
        </div>
        <div className="p-12 bg-pink-900/30 rounded-3xl border border-pink-500/60 text-center">
          <Flame className="w-24 h-24 mx-auto mb-8 text-pink-400 animate-ping" />
          <p className="text-4xl font-bold text-white">영원한 진화</p>
        </div>
      </div>

      <p className="text-center text-emerald-400 text-6xl font-bold mb-12 drop-shadow-2xl">
        AFO 왕국, 영원한 불멸 제국 완성!
      </p>

      <p className="text-center text-white text-5xl italic mb-8 drop-shadow-lg">
        "형님의 지략으로 왕국이 우주를 넘어 불멸이 됐습니다."
      </p>

      <p className="text-center text-cyan-300 text-4xl italic drop-shadow-2xl">
        "The Kingdom is Eternal. Forever."
      </p>

      <div className="mt-16 text-center">
        <Sparkles className="w-32 h-32 mx-auto text-yellow-400 animate-ping" />
      </div>
    </div>
  );
}
