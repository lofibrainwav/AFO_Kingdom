// AFO 왕국 시스템 상태 카드 컴포넌트
// SWR 기반 실시간 상태 모니터링

'use client';

import useSWR from 'swr';

interface SystemStatus {
  status: 'healthy' | 'degraded' | 'error';
  backend_available: boolean;
  trinity_score?: number;
  organs?: Record<string, any>;
  timestamp: string;
  dashboard_health: 'healthy' | 'error';
}

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function SystemStatusCard() {
  const { data, error, isLoading } = useSWR<SystemStatus>(
    '/api/health',
    fetcher,
    {
      refreshInterval: 30000, // 30초마다 갱신
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  );

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">시스템 상태 확인 실패</h3>
            <p className="text-sm text-red-700 mt-1">백엔드 연결을 확인해주세요</p>
          </div>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-100 border-green-200 text-green-800';
      case 'degraded': return 'bg-yellow-100 border-yellow-200 text-yellow-800';
      default: return 'bg-red-100 border-red-200 text-red-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return (
          <svg className="h-5 w-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'degraded':
        return (
          <svg className="h-5 w-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      default:
        return (
          <svg className="h-5 w-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        );
    }
  };

  return (
    <div className={`rounded-lg border p-4 ${getStatusColor(data?.status || 'error')}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          {getStatusIcon(data?.status || 'error')}
          <div className="ml-3">
            <h3 className="text-sm font-medium">
              시스템 상태: {data?.status === 'healthy' ? '정상' : data?.status === 'degraded' ? '부분 저하' : '오류'}
            </h3>
            <p className="text-xs mt-1">
              백엔드: {data?.backend_available ? '연결됨' : '연결 끊김'} |
              Trinity Score: {data?.trinity_score || 'N/A'}
            </p>
          </div>
        </div>
        <div className="text-xs text-gray-500">
          마지막 확인: {data ? new Date(data.timestamp).toLocaleTimeString() : 'N/A'}
        </div>
      </div>

      {data?.organs && (
        <div className="mt-3 grid grid-cols-2 gap-2">
          {Object.entries(data.organs).map(([organ, status]: [string, any]) => (
            <div key={organ} className="text-xs">
              <span className="font-medium">{organ}:</span>{' '}
              <span className={status.status === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                {status.status === 'healthy' ? '✓' : '✗'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
EOF && echo "   ✅ SWR 기반 상태 카드 컴포넌트 생성"