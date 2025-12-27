# AFO 왕국 헬스체크 SSOT 표준

## 바닥 진실 (봉인됨)

### 엔드포인트 표준
- **Dashboard**: `GET /api/health` - 백엔드 가용성 + 대시보드 상태
- **Backend**: `GET /api/health/comprehensive` - Trinity Score + 5개 오장육부

### 상태 정의
- **healthy**: 모든 시스템 정상 작동
- **degraded**: 일부 시스템 저하되나 핵심 기능 작동
- **error**: 핵심 시스템 실패 또는 연결 불가

### Green 조건 (SSOT)
둘 다 OK면 Green:
- `/api/health` 응답: `status` in ['healthy', 'degraded']
- `/api/health/comprehensive` 응답: `status` in ['healthy', 'degraded']

### 5개 오장육부 (Backend Health)
1. **心_Redis**: 세션/캐시 저장소
2. **肝_PostgreSQL**: 메인 데이터베이스
3. **脾_Ollama**: AI 모델 서빙
4. **肺_Qdrant**: 벡터 데이터베이스
5. **肾_MCP**: 외부 서비스 연결

### 응답 스키마 표준

#### Dashboard /api/health
```json
{
  "status": "healthy" | "degraded" | "error",
  "backend_available": boolean,
  "trinity_score": number | null,
  "organs": {
    "心_Redis": {"status": "healthy" | "error"},
    "肝_PostgreSQL": {"status": "healthy" | "error"},
    "脾_Ollama": {"status": "healthy" | "error"},
    "肺_Qdrant": {"status": "healthy" | "error"},
    "肾_MCP": {"status": "healthy" | "error"}
  },
  "timestamp": "ISO8601",
  "dashboard_health": "healthy" | "error"
}
```

#### Backend /api/health/comprehensive
```json
{
  "status": "healthy" | "degraded" | "error",
  "timestamp": "ISO8601",
  "organs": {
    "心_Redis": {
      "status": "healthy" | "error",
      "output": "PING -> True",
      "response_time": 0.001
    },
    "肝_PostgreSQL": {
      "status": "healthy" | "error", 
      "output": "SELECT 1 -> 1",
      "response_time": 0.005
    },
    "脾_Ollama": {
      "status": "healthy" | "error",
      "output": "ollama version",
      "response_time": 0.010
    },
    "肺_Qdrant": {
      "status": "healthy" | "error",
      "output": "collections list",
      "response_time": 0.003
    },
    "肾_MCP": {
      "status": "healthy" | "error",
      "output": "initialize -> OK",
      "response_time": 0.050
    }
  },
  "trinity_score": 0.95,
  "overall_response_time": 0.069
}
```

### 구현 원칙
1. **타임아웃**: 각 헬스체크 5초 이내 완료
2. **독립성**: 한 오장육부 실패해도 다른 체크 계속 진행
3. **캐싱**: 대시보드에서 30초 캐시 (서버 사이드)
4. **로깅**: 헬스체크 실패 시 warning 레벨 로깅

### 모니터링 통합
- **systemd**: `curl -f http://localhost:8010/api/health/comprehensive`
- **CI/CD**: 헬스체크 통과 필수
- **Dashboard**: 실시간 상태 표시 (SWR 기반)
- **Alerting**: degraded/error 상태 시 알림

### 변경 정책
- 이 문서는 SSOT로 봉인됨
- 변경 시 Trinity Score ≥ 90 AND Risk ≤ 10 검증 필수
- 변경 이력은 `docs/AFO_EVOLUTION_LOG.md`에 기록
EOF && echo "   ✅ 헬스체크 SSOT 표준 문서 생성: docs/health/SSOT_HEALTH_STANDARD.md"