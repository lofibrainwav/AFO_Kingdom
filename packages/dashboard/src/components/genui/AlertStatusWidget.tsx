// genui/AlertStatusWidget.tsx (알림 상태 위젯)
'use client';

export function AlertStatusWidget() {
  return (
    <div className="glass-card p-8 bg-gradient-to-br from-red-900/30 to-orange-900/30 rounded-3xl border border-red-500/30">
      <h3 className="text-2xl font-bold text-red-400 mb-6">Alertmanager 상태</h3>
      <div className="flex items-center gap-4 mb-4">
        <div className="w-4 h-4 rounded-full bg-emerald-500 animate-pulse"></div>
        <p className="text-emerald-400 text-xl">현재 활성 알림: 0</p>
      </div>
      <p className="text-white/90 mb-6">모든 시스템 정상 – 왕국 안전!</p>
      <div className="space-y-2 text-sm text-white/60 bg-black/20 p-4 rounded-xl">
        <p>• High CPU Usage (Critical)</p>
        <p>• OOM Risk (Warning)</p>
        <p>• API Latency (Warning)</p>
        <p>• Risk Score High (Warning)</p>
      </div>
      <p className="text-white/70 mt-6 italic text-center text-sm">
        "문제 생기면 Slack/PagerDuty로 즉시 알림 – 형님 평온 지킴!"
      </p>
    </div>
  );
}
