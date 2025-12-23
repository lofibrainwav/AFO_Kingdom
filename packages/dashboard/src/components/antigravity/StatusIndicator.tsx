"use client";

import { Activity, Bell, BellOff, Wifi, WifiOff } from 'lucide-react';
import { VerdictEvent } from '../../lib/useVerdictStream';

interface StatusIndicatorProps {
  connected: boolean;
  latestVerdict?: VerdictEvent | null;
  notificationEnabled?: boolean;
  onToggleNotifications?: () => void;
}

export default function StatusIndicator({
  connected,
  latestVerdict,
  notificationEnabled = false,
  onToggleNotifications
}: StatusIndicatorProps) {
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return '방금 전';
    if (diffMins < 60) return `${diffMins}분 전`;

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}시간 전`;

    return date.toLocaleDateString('ko-KR');
  };

  const getVerdictColor = (decision?: string) => {
    if (!decision) return 'text-gray-400';
    if (decision === 'AUTO_RUN') return 'text-green-400';
    if (decision === 'VETO') return 'text-red-400';
    return 'text-yellow-400';
  };

  const getVerdictIcon = (decision?: string) => {
    if (!decision) return <Activity className="w-3 h-3" />;
    if (decision === 'AUTO_RUN') return '🚀';
    if (decision === 'VETO') return '🚫';
    return '⏳';
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className="bg-gray-900/95 backdrop-blur-sm border border-gray-700 rounded-lg shadow-lg overflow-hidden min-w-[280px]">
        {/* 헤더 */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            {connected ? (
              <Wifi className="w-4 h-4 text-green-400" />
            ) : (
              <WifiOff className="w-4 h-4 text-red-400" />
            )}
            <span className="text-xs font-medium text-white">
              왕국의 신경계
            </span>
          </div>
          <button
            onClick={onToggleNotifications}
            className={`p-1 rounded transition-colors ${
              notificationEnabled
                ? 'text-blue-400 hover:bg-blue-500/20'
                : 'text-gray-400 hover:bg-gray-500/20'
            }`}
            title={notificationEnabled ? '알림 끄기' : '알림 켜기'}
          >
            {notificationEnabled ? (
              <Bell className="w-3 h-3" />
            ) : (
              <BellOff className="w-3 h-3" />
            )}
          </button>
        </div>

        {/* 상태 내용 */}
        <div className="px-3 py-2">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-gray-400">연결 상태</span>
            <span className={`text-xs font-medium ${
              connected ? 'text-green-400' : 'text-red-400'
            }`}>
              {connected ? '실시간 연결' : '연결 끊김'}
            </span>
          </div>

          {latestVerdict && (
            <div className="border-t border-gray-700 pt-2">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-gray-400">최근 Verdict</span>
                <span className="text-xs text-gray-500">
                  {formatTimestamp(latestVerdict.timestamp)}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm">{getVerdictIcon(latestVerdict.decision)}</span>
                <div className="flex-1 min-w-0">
                  <div className={`text-xs font-medium truncate ${getVerdictColor(latestVerdict.decision)}`}>
                    {latestVerdict.decision || 'UNKNOWN'}
                  </div>
                  <div className="text-xs text-gray-500">
                    Score: {latestVerdict.trinity_score}/100
                  </div>
                </div>
              </div>
              {latestVerdict.veto_triggered && (
                <div className="mt-1 px-2 py-1 bg-red-500/10 border border-red-500/20 rounded text-xs text-red-400">
                  헌법 개정안 0001: VETO 발동
                </div>
              )}
            </div>
          )}

          {!latestVerdict && connected && (
            <div className="border-t border-gray-700 pt-2">
              <div className="text-xs text-gray-500 text-center py-2">
                Verdict 대기 중...
              </div>
            </div>
          )}
        </div>

        {/* 푸터 - 헌법 준수 표시 */}
        <div className="px-3 py-2 border-t border-gray-700 bg-gray-800/50">
          <div className="flex items-center justify-center space-x-1">
            <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-gray-400">
              헌법 v1.0 + Amendment 0001 준수
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
