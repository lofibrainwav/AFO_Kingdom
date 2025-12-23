"use client";

import { AlertTriangle, Clock, Crown, Heart, Infinity, Palette, Shield, X } from 'lucide-react';
import { VerdictEvent } from '../../types/verdict';

interface VerdictLogModalProps {
  isOpen: boolean;
  onClose: () => void;
  pillar: string;
  verdictEvents: VerdictEvent[];
}

// 기둥별 설정
const PILLAR_CONFIG = {
  truth: {
    icon: Crown,
    label: '眞 Truth',
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/10 border-blue-500/50',
    description: '기술적 정확성, 타입 안전성, 검증 무결성'
  },
  goodness: {
    icon: Shield,
    label: '善 Goodness',
    color: 'text-green-400',
    bgColor: 'bg-green-500/10 border-green-500/50',
    description: '윤리적 타당성, 보안, 비용 효율성'
  },
  beauty: {
    icon: Palette,
    label: '美 Beauty',
    color: 'text-purple-400',
    bgColor: 'bg-purple-500/10 border-purple-500/50',
    description: '구조적 단순함, 모듈화, 일관된 API'
  },
  serenity: {
    icon: Heart,
    label: '孝 Serenity',
    color: 'text-pink-400',
    bgColor: 'bg-pink-500/10 border-pink-500/50',
    description: '사용자 마찰 제거, 자동화, 실패 복구'
  },
  eternity: {
    icon: Infinity,
    label: '永 Eternity',
    color: 'text-cyan-400',
    bgColor: 'bg-cyan-500/10 border-cyan-500/50',
    description: '재현 가능성, 문서화, 버전/결정 기록'
  },
};

export default function VerdictLogModal({
  isOpen,
  onClose,
  pillar,
  verdictEvents
}: VerdictLogModalProps) {
  if (!isOpen) return null;

  const pillarConfig = PILLAR_CONFIG[pillar as keyof typeof PILLAR_CONFIG];
  if (!pillarConfig) return null;

  const IconComponent = pillarConfig.icon;

  // 해당 pillar의 verdict 이벤트 필터링 (심층 필터링)
  const pillarEvents = verdictEvents.filter(event => {
    // Graph node ID에 pillar 포함
    if (event.graph_node_id?.toLowerCase().includes(pillar.toLowerCase())) {
      return true;
    }
    // Rule ID에 pillar 포함
    if (event.rule_id?.toLowerCase().includes(pillar.toLowerCase())) {
      return true;
    }
    // Decision에 pillar 관련 키워드 포함
    if (event.decision?.toLowerCase().includes(pillar.toLowerCase())) {
      return true;
    }
    // Type에 pillar 포함 (확장성)
    if ((event as any).type?.toLowerCase().includes(pillar.toLowerCase())) {
      return true;
    }
    return false;
  });

  // 최신 이벤트부터 정렬 (최근 200개 유지)
  const sortedEvents = [...pillarEvents]
    .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
    .slice(0, 200); // 최대 200개로 제한

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getDecisionColor = (decision?: string) => {
    if (!decision) return 'text-gray-400';
    if (decision.includes('AUTO_RUN')) return 'text-green-400';
    if (decision.includes('VETO')) return 'text-red-400';
    if (decision.includes('MANUAL')) return 'text-yellow-400';
    return 'text-gray-400';
  };

  const getDecisionIcon = (decision?: string) => {
    if (!decision) return <Clock className="w-4 h-4" />;
    if (decision.includes('AUTO_RUN')) return <Shield className="w-4 h-4" />;
    if (decision.includes('VETO')) return <AlertTriangle className="w-4 h-4" />;
    return <Clock className="w-4 h-4" />;
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-2 md:p-4">
      <div className="bg-gray-900 border border-gray-700 rounded-lg shadow-2xl max-w-4xl w-full max-h-[85vh] md:max-h-[80vh] overflow-hidden">
        {/* 헤더 */}
        <div className={`${pillarConfig.bgColor} p-6 border-b border-gray-700`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <IconComponent className={`w-8 h-8 ${pillarConfig.color}`} />
              <div>
                <h2 className="text-2xl font-bold text-white">
                  {pillarConfig.label} Verdict Logs
                </h2>
                <p className="text-gray-300 text-sm mt-1">
                  {pillarConfig.description}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* 컨텐츠 */}
        <div className="p-6 overflow-y-auto max-h-96">
          {sortedEvents.length === 0 ? (
            <div className="text-center py-12">
              <IconComponent className={`w-16 h-16 ${pillarConfig.color} mx-auto mb-4 opacity-50`} />
              <h3 className="text-lg font-semibold text-gray-400 mb-2">
                Verdict 로그가 없습니다
              </h3>
              <p className="text-gray-500">
                {pillarConfig.label}에 대한 Chancellor Graph 실행 결과가 아직 없습니다.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                  최근 {sortedEvents.length}개 Verdict 로그
                </h3>
                <div className="text-sm text-gray-400">
                  헌법 v1.0 준수 평가 결과
                </div>
              </div>

              {sortedEvents.map((event, index) => (
                <div
                  key={`${event.trace_id}-${index}`}
                  className="bg-gray-800/50 border border-gray-700 rounded-lg p-4"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      {getDecisionIcon(event.decision)}
                      <div>
                        <div className={`font-semibold ${getDecisionColor(event.decision)}`}>
                          {event.decision || 'PENDING'}
                        </div>
                        <div className="text-xs text-gray-500">
                          {event.rule_id && `Rule: ${event.rule_id}`}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-gray-400">
                        {formatTimestamp(event.timestamp)}
                      </div>
                      <div className="text-xs text-gray-500">
                        {event.trace_id}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-400">
                        {event.risk_score}
                      </div>
                      <div className="text-xs text-gray-400">Risk Score</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-400">
                        {event.trinity_score}
                      </div>
                      <div className="text-xs text-gray-400">Trinity Score</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-gray-400">Graph Node</div>
                      <div className="text-sm font-mono text-gray-300">
                        {event.graph_node_id || 'N/A'}
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-gray-400">Step</div>
                      <div className="text-sm font-mono text-gray-300">
                        {event.step}
                      </div>
                    </div>
                  </div>

                  {event.veto_triggered && (
                    <div className="bg-red-500/10 border border-red-500/50 rounded p-2">
                      <div className="flex items-center space-x-2">
                        <AlertTriangle className="w-4 h-4 text-red-400" />
                        <span className="text-red-400 text-sm font-semibold">
                          Veto Triggered - Commander Approval Required
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 푸터 */}
        <div className="bg-gray-800/50 p-4 border-t border-gray-700">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-400">
              헌법 v1.0 + Amendment 0001 준수 평가 결과
            </div>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
