/**
 * API 호출 커스텀 훅
 * AFO Kingdom Dashboard - Unified API Hook
 */

import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api-client';
import type { LoadingState, ErrorState } from '@/types/common';

interface UseApiOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: ErrorState) => void;
  refetchInterval?: number;
}

interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: ErrorState | null;
  state: LoadingState;
  refetch: () => Promise<void>;
}

/**
 * API 호출을 위한 커스텀 훅
 */
export function useApi<T = unknown>(
  endpoint: string,
  options: UseApiOptions<T> = {}
): UseApiResult<T> {
  const { immediate = true, onSuccess, onError, refetchInterval } = options;

  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState<ErrorState | null>(null);
  const [state, setState] = useState<LoadingState>(immediate ? 'loading' : 'idle');

  const fetchData = useCallback(async () => {
    setLoading(true);
    setState('loading');
    setError(null);

    try {
      const result = await apiClient.get<T>(endpoint);
      setData(result);
      setState('success');
      onSuccess?.(result);
    } catch (err) {
      const errorState: ErrorState = {
        message: err instanceof Error ? err.message : 'Unknown error',
        details: err,
      };
      setError(errorState);
      setState('error');
      onError?.(errorState);
    } finally {
      setLoading(false);
    }
  }, [endpoint, onSuccess, onError]);

  useEffect(() => {
    if (immediate) {
      fetchData();
    }
  }, [immediate, fetchData]);

  useEffect(() => {
    if (refetchInterval && refetchInterval > 0) {
      const interval = setInterval(fetchData, refetchInterval);
      return () => clearInterval(interval);
    }
  }, [refetchInterval, fetchData]);

  return {
    data,
    loading,
    error,
    state,
    refetch: fetchData,
  };
}

/**
 * POST 요청을 위한 커스텀 훅
 */
export function useApiPost<T = unknown, P = unknown>(
  endpoint: string,
  options: UseApiOptions<T> = {}
) {
  const { onSuccess, onError } = options;

  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ErrorState | null>(null);
  const [state, setState] = useState<LoadingState>('idle');

  const execute = useCallback(
    async (payload: P) => {
      setLoading(true);
      setState('loading');
      setError(null);

      try {
        const result = await apiClient.post<T>(endpoint, payload);
        setData(result);
        setState('success');
        onSuccess?.(result);
        return result;
      } catch (err) {
        const errorState: ErrorState = {
          message: err instanceof Error ? err.message : 'Unknown error',
          details: err,
        };
        setError(errorState);
        setState('error');
        onError?.(errorState);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [endpoint, onSuccess, onError]
  );

  return {
    data,
    loading,
    error,
    state,
    execute,
  };
}

