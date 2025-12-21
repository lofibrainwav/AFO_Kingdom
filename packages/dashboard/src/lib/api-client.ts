/**
 * 통합 API 클라이언트
 * AFO Kingdom Dashboard - Centralized API Client
 * 
 * 眞 (Truth): 타입 안전성 보장
 * 善 (Goodness): 에러 처리 및 재시도 로직
 * 美 (Beauty): 깔끔한 인터페이스
 * 孝 (Serenity): Zero Friction - 사용하기 쉬운 API
 */

import type { ApiResponse, ApiClientOptions } from '@/types/common';

const DEFAULT_OPTIONS: Required<ApiClientOptions> = {
  timeout: 30000, // 30초
  retries: 2,
  retryDelay: 1000, // 1초
  headers: {
    'Content-Type': 'application/json',
  },
};

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * 통합 API 클라이언트 클래스
 */
export class ApiClient {
  private baseUrl: string;
  private defaultOptions: Required<ApiClientOptions>;

  constructor(baseUrl = '', options: ApiClientOptions = {}) {
    this.baseUrl = baseUrl;
    this.defaultOptions = { ...DEFAULT_OPTIONS, ...options };
  }

  /**
   * GET 요청
   */
  async get<T = unknown>(
    endpoint: string,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>('GET', endpoint, undefined, options);
  }

  /**
   * POST 요청
   */
  async post<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>('POST', endpoint, body, options);
  }

  /**
   * PUT 요청
   */
  async put<T = unknown>(
    endpoint: string,
    body?: unknown,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>('PUT', endpoint, body, options);
  }

  /**
   * DELETE 요청
   */
  async delete<T = unknown>(
    endpoint: string,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>('DELETE', endpoint, undefined, options);
  }

  /**
   * 핵심 요청 메서드
   */
  private async request<T>(
    method: string,
    endpoint: string,
    body?: unknown,
    options?: ApiClientOptions
  ): Promise<T> {
    const opts = { ...this.defaultOptions, ...options };
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseUrl}${endpoint}`;

    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= opts.retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), opts.timeout);

        const response = await fetch(url, {
          method,
          headers: opts.headers,
          body: body ? JSON.stringify(body) : undefined,
          signal: controller.signal,
          cache: 'no-store',
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          const errorText = await response.text().catch(() => 'Unknown error');
          throw new ApiError(
            `API Error: ${response.statusText}`,
            response.status,
            errorText
          );
        }

        const data = await response.json();
        return data as T;
      } catch (error) {
        lastError = error instanceof Error ? error : new Error('Unknown error');

        // AbortError는 재시도하지 않음
        if (error instanceof Error && error.name === 'AbortError') {
          throw new ApiError('Request timeout', 504);
        }

        // 마지막 시도가 아니면 재시도
        if (attempt < opts.retries) {
          await new Promise((resolve) => setTimeout(resolve, opts.retryDelay));
          continue;
        }
      }
    }

    throw lastError || new ApiError('Request failed');
  }
}

/**
 * 기본 API 클라이언트 인스턴스
 */
export const apiClient = new ApiClient('');

/**
 * 백엔드 API 클라이언트 (포트 8010)
 */
export const backendApi = new ApiClient(
  process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010',
  {
    timeout: 300000, // 5분 (LLM 호출용)
  }
);

/**
 * 헬퍼 함수들
 */
export async function fetchWithErrorHandling<T>(
  fn: () => Promise<T>,
  errorMessage = 'Failed to fetch data'
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      errorMessage,
      undefined,
      error instanceof Error ? error.message : 'Unknown error'
    );
  }
}

