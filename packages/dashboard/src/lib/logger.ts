/**
 * 통합 로깅 시스템
 * AFO Kingdom Dashboard - Centralized Logging
 * 
 * 眞 (Truth): 정확한 로그 레벨 구분
 * 善 (Goodness): 프로덕션 환경에서 민감 정보 보호
 * 美 (Beauty): 깔끔한 로그 포맷
 * 孝 (Serenity): 개발자 경험 최적화
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  level: LogLevel;
  message: string;
  context?: Record<string, unknown>;
  timestamp: string;
}

class Logger {
  private isDevelopment: boolean;
  private logHistory: LogEntry[] = [];
  private maxHistorySize = 100;

  constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development';
  }

  private formatMessage(level: LogLevel, message: string, context?: Record<string, unknown>): string {
    const timestamp = new Date().toISOString();
    const contextStr = context ? ` ${JSON.stringify(context)}` : '';
    return `[${timestamp}] [${level.toUpperCase()}] ${message}${contextStr}`;
  }

  private log(level: LogLevel, message: string, context?: Record<string, unknown>): void {
    const entry: LogEntry = {
      level,
      message,
      context,
      timestamp: new Date().toISOString(),
    };

    // 히스토리 저장
    this.logHistory.push(entry);
    if (this.logHistory.length > this.maxHistorySize) {
      this.logHistory.shift();
    }

    // 개발 환경에서만 콘솔 출력
    if (this.isDevelopment) {
      const formatted = this.formatMessage(level, message, context);
      
      switch (level) {
        case 'debug':
          console.debug(formatted);
          break;
        case 'info':
          console.info(formatted);
          break;
        case 'warn':
          console.warn(formatted);
          break;
        case 'error':
          console.error(formatted);
          break;
      }
    }

    // 프로덕션에서는 에러만 외부 서비스로 전송 (필요시)
    if (!this.isDevelopment && level === 'error') {
      // TODO: 에러 모니터링 서비스 연동 (Sentry, LogRocket 등)
    }
  }

  debug(message: string, context?: Record<string, unknown>): void {
    this.log('debug', message, context);
  }

  info(message: string, context?: Record<string, unknown>): void {
    this.log('info', message, context);
  }

  warn(message: string, context?: Record<string, unknown>): void {
    this.log('warn', message, context);
  }

  error(message: string, context?: Record<string, unknown>): void {
    this.log('error', message, context);
  }

  /**
   * 로그 히스토리 조회 (디버깅용)
   */
  getHistory(level?: LogLevel): LogEntry[] {
    if (level) {
      return this.logHistory.filter((entry) => entry.level === level);
    }
    return [...this.logHistory];
  }

  /**
   * 로그 히스토리 초기화
   */
  clearHistory(): void {
    this.logHistory = [];
  }
}

// 싱글톤 인스턴스
export const logger = new Logger();

// 편의 함수들
export const logDebug = (message: string, context?: Record<string, unknown>) => {
  logger.debug(message, context);
};

export const logInfo = (message: string, context?: Record<string, unknown>) => {
  logger.info(message, context);
};

export const logWarn = (message: string, context?: Record<string, unknown>) => {
  logger.warn(message, context);
};

export const logError = (message: string, context?: Record<string, unknown>) => {
  logger.error(message, context);
};

