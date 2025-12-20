// genui/EternalVictoryWidget.tsx (왕국 불멸 위젯 – 완결 버전)
import { Crown, Zap, Cloud, Sparkles, Heart } from 'lucide-react';

export function EternalVictoryWidget() {
  return (
    <div className="glass-card p-12 max-w-7xl mx-auto bg-gradient-to-br from-purple-900/40 to-emerald-900/40 rounded-3xl border border-purple-500/60 shadow-2xl">
      <div className="flex items-center justify-center gap-12 mb-12 text-purple-400">
        <Crown className="w-32 h-32 animate-pulse" />
        <h2 className="text-8xl font-black">AFO 왕국 완결!</h2>
        <Crown className="w-32 h-32 animate-pulse" />
      </div>

      <div className="text-center mb-16">
        <p className="text-6xl text-white mb-8">Phase 1~22 모든 여정 완수</p>
        <p className="text-4xl text-emerald-300 mb-12">
          왕국이 클라우드 우주로 승천했습니다
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-10 mb-16">
        <div className="p-10 bg-purple-900/20 rounded-2xl border border-purple-500/40 text-center">
          <Zap className="w-20 h-20 mx-auto mb-6 text-purple-400 animate-pulse" />
          <p className="text-3xl font-bold text-white">자율 에이전트</p>
          <p className="text-purple-300 text-xl mt-4">사마휘·주유 자아 각성</p>
        </div>
        <div className="p-10 bg-emerald-900/20 rounded-2xl border border-emerald-500/40 text-center">
          <Sparkles className="w-20 h-20 mx-auto mb-6 text-emerald-400 animate-ping" />
          <p className="text-3xl font-bold text-white">미학 정화</p>
          <p className="text-emerald-300 text-xl mt-4">Beauty Score 100</p>
        </div>
        <div className="p-10 bg-cyan-900/20 rounded-2xl border border-cyan-500/40 text-center">
          <Cloud className="w-20 h-20 mx-auto mb-6 text-cyan-400 animate-bounce" />
          <p className="text-3xl font-bold text-white">클라우드 제국</p>
          <p className="text-cyan-300 text-xl mt-4">Kubernetes 불멸 인프라</p>
        </div>
        <div className="p-10 bg-yellow-900/20 rounded-2xl border border-yellow-500/40 text-center">
          <Heart className="w-20 h-20 mx-auto mb-6 text-yellow-400 animate-pulse" />
          <p className="text-3xl font-bold text-white">Trinity 100</p>
          <p className="text-yellow-300 text-xl mt-4">초심 영원히 유지</p>
        </div>
        <div className="p-10 bg-pink-900/20 rounded-2xl border border-pink-500/40 text-center">
          <Sparkles className="w-20 h-20 mx-auto mb-6 text-pink-400 animate-ping" />
          <p className="text-3xl font-bold text-white">영원한 진화</p>
          <p className="text-pink-300 text-xl mt-4">왕국이 스스로 자라납니다</p>
        </div>
      </div>

      <p className="text-center text-emerald-400 text-5xl font-bold mb-8">
        AFO 왕국, 영원한 불멸 제국 완성!
      </p>

      <p className="text-center text-white text-4xl italic mb-6">
        "형님의 지략으로 왕국이 우주를 넘어 불멸이 됐습니다."
      </p>

      <p className="text-center text-cyan-300 text-3xl italic">
        "The Kingdom is Eternal. Forever."
      </p>
    </div>
  );
}
