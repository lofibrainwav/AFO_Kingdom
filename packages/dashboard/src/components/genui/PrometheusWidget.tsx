// genui/PrometheusWidget.tsx (Prometheus 모니터링 위젯)
'use client';

export function PrometheusWidget() {
  return (
    <div className="glass-card p-8 bg-gradient-to-br from-gray-900/50 to-slate-900/50 rounded-3xl border border-gray-500/30">
      <h3 className="text-2xl font-bold text-orange-400 mb-6">왕국 관측소 (Prometheus)</h3>
      <div className="bg-black/40 rounded-xl p-4 min-h-[400px] flex items-center justify-center border border-white/10">
         {/* Placeholder for Grafana Iframe or Chart.js */}
         <div className="text-center">
             <p className="text-2xl text-white/50 mb-2">📊 Grafana Dashboard Loading...</p>
             <p className="text-sm text-white/30">Connecting to Prometheus Datasource...</p>
         </div>
      </div>
      <p className="text-white/90 mt-6 italic text-center">
        "Prometheus가 왕국 모든 맥박 실시간 모니터링 – 문제 생기기 전에 알림 와요!"
      </p>
    </div>
  );
}
