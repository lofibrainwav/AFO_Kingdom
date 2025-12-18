# API 엔드포인트 참조 문서

## 📋 개요

AFO Kingdom Soul Engine API의 모든 엔드포인트 통합 참조 문서입니다.

**Base URL**: `http://localhost:8010` (기본값)  
**API Version**: `6.3.0`  
**OpenAPI Docs**: `http://localhost:8010/docs`

---

## 📊 엔드포인트 통계

- **총 엔드포인트**: 49개 (메인 엔드포인트)
- **HTTP 메서드**: GET, POST, PUT, DELETE, PATCH
- **인증**: 선택적 (대부분 공개)
- **카테고리**: 12개

---

## 🏷️ 엔드포인트 카테고리

### 1. Health & System (건강 체크)

#### `GET /`
**설명**: API 루트 엔드포인트 - API 정보 반환

**응답**:
```json
{
  "name": "AFO Kingdom Soul Engine API",
  "version": "6.3.0",
  "description": "眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)",
  "status": "running"
}
```

#### `GET /health`
**설명**: 시스템 건강 체크 (Trinity Score 기반)

**응답**:
```json
{
  "status": "healthy",
  "trinity_score": {
    "truth": 89,
    "goodness": 85,
    "beauty": 72,
    "serenity": 95,
    "overall": 84
  }
}
```

#### `GET /api/system/metrics`
**설명**: 시스템 메트릭 조회

#### `GET /api/system/logs/stream`
**설명**: 로그 스트리밍 (SSE)

---

### 2. Chancellor (승상 시스템)

#### `POST /chancellor/invoke`
**설명**: Chancellor Graph 호출 (LangGraph 기반 3책사 조율)

**요청**:
```json
{
  "message": "사용자 메시지",
  "auto_run": false,
  "context": {}
}
```

**응답**:
```json
{
  "response": "승상 응답",
  "trinity_score": {
    "truth": 90,
    "goodness": 85,
    "beauty": 80,
    "serenity": 95
  },
  "strategist": "제갈량"
}
```

#### `GET /chancellor/health`
**설명**: Chancellor 시스템 건강 체크

---

### 3. Skills Registry (스킬 레지스트리)

#### `GET /api/skills/list`
**설명**: 스킬 목록 조회 (필터링, 페이지네이션)

**쿼리 파라미터**:
- `category`: 카테고리 필터
- `status`: 상태 필터
- `search`: 검색어 (이름/설명)
- `min_philosophy_avg`: 최소 철학 평균 점수
- `execution_mode`: 실행 모드 필터
- `offset`: 페이지 시작 위치 (기본: 0)
- `limit`: 페이지 크기 (기본: 50, 최대: 100)

**응답**:
```json
{
  "skills": [
    {
      "skill_id": "skill_001_youtube_spec_gen",
      "name": "YouTube to n8n Spec Generator",
      "category": "workflow_automation",
      "philosophy_scores": {
        "truth": 95,
        "goodness": 90,
        "beauty": 92,
        "serenity": 88
      }
    }
  ],
  "total": 19,
  "offset": 0,
  "limit": 50
}
```

#### `GET /api/skills/{skill_id}`
**설명**: 스킬 상세 조회

#### `POST /api/skills/`
**설명**: 스킬 등록

**요청**:
```json
{
  "skill_id": "skill_xxx",
  "name": "스킬 이름",
  "description": "스킬 설명",
  "category": "strategic_command",
  "philosophy_scores": {
    "truth": 90,
    "goodness": 85,
    "beauty": 80,
    "serenity": 95
  }
}
```

#### `POST /api/skills/{skill_id}/execute`
**설명**: 스킬 실행

**요청**:
```json
{
  "parameters": {
    "param1": "value1"
  }
}
```

#### `DELETE /api/skills/{skill_id}`
**설명**: 스킬 삭제

#### `GET /api/skills/stats`
**설명**: 스킬 통계 조회

#### `GET /api/skills/categories`
**설명**: 카테고리 목록 조회

#### `GET /api/skills/health`
**설명**: 스킬 서비스 헬스체크

---

### 4. 5 Pillars (眞善美孝永)

#### `GET /api/5pillars/current`
**설명**: 현재 5기둥 점수 조회

**응답**:
```json
{
  "truth": 89,
  "goodness": 85,
  "beauty": 72,
  "serenity": 95,
  "eternity": 90,
  "overall": 84.2
}
```

#### `POST /api/5pillars/live`
**설명**: LangFlow 실시간 5기둥 평가

#### `GET /api/5pillars/family/hub`
**설명**: 가족 허브 전체 상태 조회

#### `POST /api/5pillars/family/hub/member/update`
**설명**: 가족 구성원 데이터 업데이트

#### `GET /api/5pillars/family/hub/data`
**설명**: 실시간 가족 허브 데이터 조회

---

### 5. RAG (Retrieval-Augmented Generation)

#### `POST /api/crag`
**설명**: CRAG (Corrective RAG) 질의 - 문서 채점 + 웹 검색 fallback

**요청**:
```json
{
  "query": "사용자 질의",
  "top_k": 5
}
```

**응답**:
```json
{
  "answer": "생성된 답변",
  "sources": [
    {
      "document": "문서 내용",
      "score": 0.95
    }
  ],
  "trinity_score": {
    "truth": 92,
    "goodness": 88,
    "beauty": 85,
    "serenity": 90
  }
}
```

---

### 6. Family Hub (가족 허브)

#### `GET /family/`
**설명**: 가족 허브 메인 페이지

#### `GET /family/members`
**설명**: 가족 구성원 목록

#### `POST /family/members`
**설명**: 가족 구성원 추가

#### `POST /family/activity`
**설명**: 가족 활동 기록

#### `GET /family/timeline`
**설명**: 가족 타임라인 조회

#### `GET /family/happiness`
**설명**: 가족 행복도 조회

#### `GET /family/health`
**설명**: 가족 허브 건강 체크

---

### 7. Authentication (인증)

#### `POST /api/auth/login`
**설명**: 사용자 로그인

**요청**:
```json
{
  "username": "사용자명",
  "password": "비밀번호"
}
```

#### `POST /api/auth/verify`
**설명**: 토큰 검증

#### `GET /api/auth/health`
**설명**: 인증 서비스 헬스체크

---

### 8. Users (사용자 관리)

#### `GET /api/users/health`
**설명**: 사용자 관리 시스템 건강 체크

#### `POST /api/users`
**설명**: 사용자 생성

#### `GET /api/users/{user_id}`
**설명**: 사용자 조회

#### `PUT /api/users/{user_id}`
**설명**: 사용자 업데이트

#### `DELETE /api/users/{user_id}`
**설명**: 사용자 삭제

---

### 9. Personas (페르소나)

#### `GET /api/personas/health`
**설명**: 페르소나 시스템 건강 체크

#### `GET /api/personas/current`
**설명**: 현재 활성 페르소나 조회

#### `GET /api/personas`
**설명**: 페르소나 목록 조회

#### `GET /api/personas/{persona_id}`
**설명**: 페르소나 상세 조회

#### `POST /api/personas/switch`
**설명**: 페르소나 전환

#### `GET /api/personas/{persona_id}/trinity-score`
**설명**: 페르소나별 Trinity Score 조회

---

### 10. Chat (채팅)

#### `POST /message`
**설명**: 채팅 메시지 전송

#### `GET /providers`
**설명**: 사용 가능한 LLM 제공자 목록

#### `GET /stats`
**설명**: 라우팅 통계 조회

#### `GET /health`
**설명**: 채팅 서비스 헬스체크

---

### 11. Julie CPA (로열 재무)

#### `GET /api/julie/status`
**설명**: Julie CPA 상태 조회

#### `GET /api/julie/dashboard`
**설명**: Julie CPA 대시보드 데이터

---

### 12. Wallet (API 지갑)

#### `POST /browser/save-token`
**설명**: 브라우저 토큰 저장

#### `GET /browser/extraction-script`
**설명**: 브라우저 추출 스크립트

---

## 🔐 인증

대부분의 엔드포인트는 공개되어 있으나, 일부 엔드포인트는 인증이 필요할 수 있습니다.

**인증 방법**:
- JWT 토큰 (Bearer Token)
- API Key (헤더에 포함)

---

## 📝 요청/응답 형식

### 요청 형식
- **Content-Type**: `application/json`
- **Accept**: `application/json`

### 응답 형식
- **성공**: HTTP 200-299
- **클라이언트 오류**: HTTP 400-499
- **서버 오류**: HTTP 500-599

### 에러 응답 형식
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "에러 메시지",
    "details": {}
  }
}
```

---

## 🎯 Trinity Score

모든 엔드포인트는 실행 시 **眞善美孝永 Trinity Score**를 반환합니다:

```json
{
  "trinity_metadata": {
    "truth": 90,
    "goodness": 85,
    "beauty": 80,
    "serenity": 95,
    "eternity": 90,
    "overall": 88.0
  }
}
```

---

## 📚 관련 문서

- [AFO Final Handover](AFO_FINAL_HANDOVER.md)
- [Skills Registry Reference](SKILLS_REGISTRY_REFERENCE.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)

---

**최종 업데이트**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom

