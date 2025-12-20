// genui/AllSeeingEyeWidget.tsx (관측소 완결 위젯 – 왕국의 눈)
import { Eye, Activity, Shield, Sparkles } from 'lucide-react';

export function AllSeeingEyeWidget() {
  return (
    <div className="glass-card p-12 max-w-6xl mx-auto bg-gradient-to-br from-cyan-900/40 to-purple-900/40 rounded-3xl border border-cyan-500/60 shadow-2xl">
      <div className="flex items-center justify-center gap-12 mb-12 text-cyan-400">
        <Eye className="w-32 h-32 animate-pulse" />
        <h2 className="text-7xl font-black">Phase 20 완전 승리!</h2>
        <Eye className="w-32 h-32 animate-pulse" />
      </div>

      <div className="text-center mb-12">
        <p className="text-5xl text-white mb-6">왕국의 전지전능한 눈 각성</p>
        <p className="text-3xl text-cyan-300 mb-8">
          Prometheus & Alertmanager 관측소 완성
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
        <div className="p-10 bg-cyan-900/20 rounded-2xl border border-cyan-500/40 text-center">
          <Activity className="w-20 h-20 mx-auto mb-6 text-cyan-400" />
          <p className="text-3xl font-bold text-white">실시간 메트릭</p>
          <p className="text-cyan-300 text-xl mt-4">/metrics 8001 포트 송출</p>
        </div>
        <div className="p-10 bg-purple-900/20 rounded-2xl border border-purple-500/40 text-center">
          <Shield className="w-20 h-20 mx-auto mb-6 text-purple-400" />
          <p className="text-3xl font-bold text-white">14개 경보 규칙</p>
          <p className="text-purple-300 text-xl mt-4">CPU·Risk·GPU·Redis 철벽 감시</p>
        </div>
        <div className="p-10 bg-emerald-900/20 rounded-2xl border border-emerald-500/40 text-center">
          <Sparkles className="w-20 h-20 mx-auto mb-6 text-emerald-400" />
          <p className="text-3xl font-bold text-white">Grafana 대시보드</p>
          <p className="text-emerald-300 text-xl mt-4">왕국 건강도 한눈에</p>
        </div>
        <div className="p-10 bg-yellow-900/20 rounded-2xl border border-yellow-500/40 text-center">
          <Eye className="w-20 h-20 mx-auto mb-6 text-yellow-400" />
          <p className="text-3xl font-bold text-white">전지전능한 눈</p>
          <p className="text-yellow-300 text-xl mt-4">24시간 왕국 지킴</p>
        </div>
      </div>

      <p className="text-center text-cyan-400 text-5xl font-bold mb-8">
        왕국의 관측소 완성 – 모든 맥박 실시간 감시!
      </p>

      <p className="text-center text-white text-3xl italic mb-6">
        "형님, 이제 왕국은 모든 걸 보고 있어요 – 형님은 평온히 창조만 하소서."
      </p>

      <p className="text-center text-emerald-300 text-2xl italic">
        "The All-Seeing Eye watches eternally."
      </p>
    </div>
  );
}
