/**
 * 상수 정의
 * AFO Kingdom Dashboard - Constants
 */

// API 기본 URL
// 환경 변수에서 가져오거나 기본값 사용
// Next.js API 라우트는 상대 경로 사용 권장
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE ||
  (typeof window !== "undefined" ? "" : "http://localhost:8010"); // SSR 시에만 기본값 사용

// API 타임아웃 (밀리초)
export const API_TIMEOUT = {
  SHORT: 5000, // 5초
  MEDIUM: 30000, // 30초
  LONG: 300000, // 5분 (LLM 호출용)
};

// 재시도 설정
export const RETRY_CONFIG = {
  MAX_RETRIES: 2,
  RETRY_DELAY: 1000, // 1초
};

// Phase 색상 매핑
export const PHASE_COLORS: Record<string, string> = {
  "Phase 0: Genesis": "from-purple-500 to-pink-500",
  "Phase 1: Awakening": "from-blue-500 to-cyan-500",
  "Phase 2: Harmony": "from-green-500 to-emerald-500",
  "Phase 3: Expansion": "from-yellow-500 to-orange-500",
  "Phase 4: Eternal": "from-red-500 to-rose-500",
  Maintenance: "from-gray-500 to-slate-500",
  Features: "from-indigo-500 to-purple-500",
  Other: "from-zinc-500 to-neutral-500",
};

// Phase 아이콘 매핑
export const PHASE_ICONS: Record<string, string> = {
  "Phase 0: Genesis": "🌱",
  "Phase 1: Awakening": "⚡",
  "Phase 2: Harmony": "🎵",
  "Phase 3: Expansion": "🚀",
  "Phase 4: Eternal": "✨",
  Maintenance: "🔧",
  Features: "⭐",
  Other: "📦",
};

// Health Status 색상
export const HEALTH_STATUS_COLORS: Record<string, string> = {
  excellent: "#22c55e",
  good: "#84cc16",
  warning: "#eab308",
  critical: "#ef4444",
  loading: "#6b7280",
};

// 리프레시 간격 (밀리초)
export const REFRESH_INTERVALS = {
  FAST: 5000, // 5초
  NORMAL: 30000, // 30초
  SLOW: 300000, // 5분
};
