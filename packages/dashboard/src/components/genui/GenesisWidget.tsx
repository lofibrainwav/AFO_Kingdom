'use client';

import { useState } from 'react';
import { Sparkles, Loader2, Send, CheckCircle2, AlertTriangle, Play, Code, Eye } from 'lucide-react';
import { logError } from '@/lib/logger';

interface CreationResult {
  code: string;
  screenshot_path: string | null;
  trinity_score: number;
  risk_score: number;
  iteration: number;
  success: boolean;
  feedback: string;
}

export function GenesisWidget() {
  const [prompt, setPrompt] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [status, setStatus] = useState<string>('');

  const handleCreate = async () => {
    if (!prompt.trim()) return;

    setIsCreating(true);
    setStatus('왕국의 지혜를 모으는 중...');
    setResult(null);

    try {
      const res = await fetch('/api/serenity/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
        setStatus(data.success ? '제네시스 성공: 새로운 차원이 열렸습니다.' : '제네시스 지연: 추가 정련이 필요합니다.');
      } else {
        const errorData = await res.json().catch(() => ({}));
        const errorMsg = errorData.detail || errorData.error || '알 수 없는 오류';
        setStatus(`제네시스 실패: ${errorMsg}`);
      }
    } catch (error) {
      logError('Genesis creation failed', { error: error instanceof Error ? error.message : 'Unknown error' });
      if (error instanceof TypeError && error.message.includes('fetch')) {
        setStatus('연결 실패: API 서버가 실행 중이지 않습니다. 포트 8010에서 서버를 시작해주세요.');
      } else {
        setStatus('연결 실패: 지휘소와의 통신이 원활하지 않습니다.');
      }
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="p-8 bg-gradient-to-br from-indigo-900/40 via-purple-900/40 to-pink-900/40 rounded-[2.5rem] border border-purple-500/30 backdrop-blur-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] transition-all duration-500 hover:shadow-purple-500/20 group">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-purple-600/20 rounded-2xl border border-purple-500/40">
            <Sparkles className="w-8 h-8 text-purple-400 animate-pulse" />
          </div>
          <div>
            <h3 className="text-2xl font-black text-white tracking-tight">프로젝트 제네시스</h3>
            <p className="text-purple-300/60 text-sm font-medium">자율 확장형 UI 창조 루프</p>
          </div>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-full border border-white/10">
          <div className={`w-2 h-2 rounded-full animate-ping ${isCreating ? 'bg-yellow-400' : 'bg-emerald-400'}`} />
          <span className="text-xs font-bold text-white/70 uppercase tracking-widest">
            {isCreating ? 'Creating' : 'Ready'}
          </span>
        </div>
      </div>

      {/* Input Area */}
      <div className="relative mb-8">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="창조하고 싶은 UI의 비전을 설명하세요... (예: '왕국의 자산을 실시간으로 감시하는 골드 테마의 대시보드')"
          className="w-full h-32 p-6 bg-black/40 border border-white/10 rounded-2xl text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-all resize-none font-medium leading-relaxed"
          disabled={isCreating}
        />
        <button
          onClick={handleCreate}
          disabled={isCreating || !prompt.trim()}
          className={`absolute bottom-4 right-4 p-4 rounded-xl transition-all duration-300 ${
            isCreating || !prompt.trim()
            ? 'bg-white/5 text-white/20'
            : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg shadow-purple-900/40 hover:scale-110 active:scale-95'
          }`}
        >
          {isCreating ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6" />}
        </button>
      </div>

      {/* Status Bar */}
      {status && (
        <div className={`mb-8 p-4 rounded-xl border flex items-center gap-3 animate-in fade-in slide-in-from-top-2 ${
          status.includes('성공') ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' :
          status.includes('실패') ? 'bg-red-500/10 border-red-500/30 text-red-300' :
          'bg-white/5 border-white/10 text-white/60'
        }`}>
          {isCreating ? <Play className="w-4 h-4 animate-pulse" /> : status.includes('성공') ? <CheckCircle2 className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
          <span className="text-sm font-bold">{status}</span>
        </div>
      )}

      {/* Result Area */}
      {result && (
        <div className="space-y-6 animate-in fade-in zoom-in-95 duration-500">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-black/40 rounded-2xl border border-white/5">
              <p className="text-[10px] uppercase tracking-widest font-black text-white/30 mb-1">Trinity Score</p>
              <p className="text-3xl font-black text-purple-400">{(result.trinity_score * 100).toFixed(1)}%</p>
            </div>
            <div className="p-4 bg-black/40 rounded-2xl border border-white/5">
              <p className="text-[10px] uppercase tracking-widest font-black text-white/30 mb-1">Risk Score</p>
              <p className="text-3xl font-black text-pink-400">{(result.risk_score * 100).toFixed(1)}%</p>
            </div>
          </div>

          <div className="bg-black/40 rounded-2xl border border-white/5 overflow-hidden">
            <div className="p-3 border-b border-white/5 flex items-center justify-between bg-white/5">
              <div className="flex items-center gap-2">
                <Code className="w-4 h-4 text-white/40" />
                <span className="text-[10px] font-bold text-white/60 uppercase tracking-widest">Generated Component</span>
              </div>
              <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">v{result.iteration}</span>
            </div>
            <pre className="p-6 text-xs text-purple-200/80 font-mono overflow-x-auto max-h-48 custom-scrollbar">
              <code>{result.code}</code>
            </pre>
          </div>

          {result.feedback && (
            <div className="p-4 bg-purple-900/20 rounded-xl border border-purple-500/20">
              <p className="text-xs font-bold text-purple-300 mb-1 flex items-center gap-2">
                <Eye className="w-3 h-3" /> 성찰 결과 (Critique)
              </p>
              <p className="text-sm text-purple-200/60 leading-relaxed italic">"{result.feedback}"</p>
            </div>
          )}
        </div>
      )}

      {/* Footer Decoration */}
      <div className="mt-8 pt-6 border-t border-white/5 flex items-center justify-center gap-3 opacity-20 group-hover:opacity-100 transition-opacity duration-500">
        <div className="h-[1px] w-12 bg-gradient-to-r from-transparent to-white" />
        <span className="text-[10px] font-black uppercase tracking-[0.3em] text-white">Self-Expanding Kingdom</span>
        <div className="h-[1px] w-12 bg-gradient-to-l from-transparent to-white" />
      </div>
    </div>
  );
}
