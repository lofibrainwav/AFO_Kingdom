# 옵시디언 템플릿 모음

> [!abstract] 템플릿 개요
> AFO Kingdom 문서화 작업을 위한 표준화된 옵시디언 템플릿 모음입니다.
> 각 템플릿은 Trinity 5기둥 철학을 기반으로 구조화되어 있습니다.

---

## 📋 템플릿 목록

### 프로젝트 문서 템플릿 (`project_doc.md`)
**용도**: 새로운 프로젝트 시작 시 사용
**포함 사항**:
- 프로젝트 개요 및 목표
- 요구사항 명세
- 아키텍처 설계 (Mermaid 다이어그램 포함)
- Trinity Score 평가 기준
- 위험 요소 및 완화 전략
- 성공 지표

**사용 방법**:
```markdown
# 프로젝트 이름 입력 후 템플릿 변수들을 채워주세요
{{project_name}} → 실제 프로젝트명
{{assignee}} → 담당자 이름
{{start_date}} → 시작일 (YYYY-MM-DD)
```

---

### 시스템 컴포넌트 템플릿 (`system_component.md`)
**용도**: 새로운 시스템 컴포넌트 설계 시 사용
**포함 사항**:
- 컴포넌트 인터페이스 설계
- 데이터 모델 및 DB 스키마
- 처리 흐름 (시퀀스/플로우차트)
- 테스트 전략
- 모니터링 및 로깅
- 보안 고려사항
- 배포 및 운영 가이드

**사용 방법**:
```markdown
# 컴포넌트 타입에 맞게 변수들을 설정하세요
{{component_name}} → 컴포넌트명 (예: UserService, AuthManager)
{{component_type}} → 타입 (api, service, worker, etc.)
{{assignee}} → 담당 개발자
```

---

### API 엔드포인트 템플릿 (`api_endpoint.md`)
**용도**: REST API 엔드포인트 설계 시 사용
**포함 사항**:
- 상세한 API 명세 (요청/응답)
- 인증 및 권한 요구사항
- 에러 응답 표준
- 처리 흐름 다이어그램
- 테스트 케이스
- 성능 요구사항
- 보안 고려사항
- 모니터링 메트릭

**사용 방법**:
```markdown
# 엔드포인트 정보 입력
{{endpoint_path}} → /api/users
{{method}} → GET, POST, PUT, DELETE
{{endpoint_name}} → UserList, UserCreate 등
```

---

### Dataview 쿼리 템플릿 (`dataview_queries.md`)
**용도**: 프로젝트 모니터링 및 메트릭 대시보드 구축
**포함 사항**:
- 프로젝트 상태 대시보드
- 태스크 관리 쿼리
- 시스템 모니터링
- 메트릭 계산
- 검증 보고서 자동화
- DataviewJS 시각화 예제

**사용 방법**:
```markdown
# Dataview 플러그인 설치 후 쿼리들을 복사해서 사용하세요
# 옵시디언 설정 → 커뮤니티 플러그인 → Dataview 검색 및 설치
```

---

### 협업 워크플로우 가이드 (`collaboration_guide.md`)
**용도**: 팀 협업 프로세스 표준화 및 자동화
**포함 사항**:
- 실시간 협업 설정 (옵시디언 Sync, Git 전략)
- 역할 기반 권한 관리 (Trinity 책사 시스템)
- PR 템플릿 및 코드 리뷰 체크리스트
- 팀 메트릭 및 KPI 대시보드
- 협업 모범 사례 및 워크플로우

**사용 방법**:
```markdown
# 팀 협업 시 반드시 적용
# Git Flow 브랜치 전략과 PR 템플릿 사용
# Dataview로 팀 생산성 모니터링
```

---

### AI 통합 가이드 (`ai_integration_guide.md`)
**용도**: AI 기반 자동화 및 지능화 시스템 구축
**포함 사항**:
- Trinity Score 기반 AI 라우팅
- 자동 문서 생성 및 코드 리뷰
- AI 메트릭 모니터링 및 비용 분석
- 멀티모달 AI 처리 및 실시간 협업
- 윤리적 AI 사용 가이드라인

**사용 방법**:
```markdown
# AI 도구 활성화 전 Trinity Score 85점 이상 확인
# 민감 데이터는 로컬 Ollama 모델 사용
# 모든 AI 응답은 인간 검토 후 적용
```

---

## 🎯 템플릿 사용 가이드

### 1. 템플릿 적용 방법

#### 옵시디언 템플릿 기능 사용
1. **옵시디언 설정 → Core plugins → Templates 활성화**
2. **설정 → Core plugins → Templates → Template folder location**: `_templates`
3. **새 문서 생성 시 템플릿 선택**

#### 수동 적용
1. **원하는 템플릿 파일 열기**
2. **내용 전체 복사 (Ctrl+A, Ctrl+C)**
3. **새 문서에 붙여넣기 (Ctrl+V)**
4. **변수들 실제 값으로 교체**

### 2. 변수 치환 규칙

| 변수 패턴 | 설명 | 예시 |
|----------|------|------|
| `{{variable_name}}` | 필수 입력 변수 | `{{project_name}}` |
| `{{variable_name}}` | 선택 입력 변수 | `{{optional_field}}` |
| `{{date:format}}` | 자동 날짜 | `{{date:YYYY-MM-DD}}` |

### 3. YAML Frontmatter 표준

모든 템플릿은 다음과 같은 Frontmatter 구조를 따릅니다:

```yaml
---
created: {{date:YYYY-MM-DD}}          # 자동 생성일
status: planning                       # 상태 (planning, in-progress, completed)
priority: medium                       # 우선순위 (high, medium, low)
tags: [tag1, tag2, tag3]              # 태그 목록
type: document_type                    # 문서 타입
---

# 문서 제목
```

---

## 🎨 디자인 원칙

### Trinity Score 기반 구조화

#### 眞 (Truth) - 기술적 정확성
- **표준화된 명세**: 일관된 API/컴포넌트 설계
- **코드 예제**: 실제 사용할 수 있는 코드 조각
- **다이어그램**: 정확한 시스템 구조 표현

#### 善 (Goodness) - 안정성과 신뢰성
- **에러 처리**: 포괄적인 예외 상황 고려
- **테스트 전략**: 다양한 테스트 케이스 포함
- **모니터링**: 메트릭 및 로깅 표준

#### 美 (Beauty) - 단순함과 우아함
- **시각적 구성**: Callout blocks와 이모지 활용
- **명확한 계층**: 적절한 제목 레벨과 구조
- **일관된 스타일**: 통일된 색상과 레이아웃

#### 孝 (Serenity) - 마찰 제거
- **템플릿 자동화**: 반복 작업 최소화
- **표준 프로세스**: 예측 가능한 워크플로우
- **사용자 친화**: 직관적인 변수명과 구조

#### 永 (Eternity) - 장기적 유지보수
- **확장성 고려**: 미래 요구사항 수용
- **문서화 표준**: 체계적인 링크 구조
- **버전 관리**: 템플릿 버전 추적

---

## 🔧 템플릿 관리

### 템플릿 업데이트 프로세스

1. **변경 검토**: 사용자 피드백 수집
2. **개선 적용**: 새로운 요구사항 반영
3. **호환성 확인**: 기존 문서 영향 평가
4. **버전 업데이트**: 템플릿 버전 증가
5. **문서화**: 변경사항 기록

### 템플릿 검증 체크리스트

- [ ] YAML Frontmatter 유효성
- [ ] 변수 치환 정상 작동
- [ ] Mermaid 다이어그램 렌더링
- [ ] Callout blocks 표시
- [ ] 링크 구조 유효성
- [ ] 모바일 환경 호환성

---

## 📊 템플릿 사용 통계

> [!stats] 템플릿 활용 현황
>
> ```dataview
> TABLE length(rows) as "사용 문서 수"
> FROM "docs"
> FLATTEN file.inlinks as inlink
> WHERE contains(inlink.path, "_templates/")
> GROUP BY inlink
> SORT length(rows) DESC
> ```

---

## 🚀 확장 계획

### 예정된 템플릿 추가

1. **배포 가이드 템플릿**
   - Docker 구성, Kubernetes 매니페스트
   - CI/CD 파이프라인 설정
   - 롤백 전략

2. **보안 감사 템플릿**
   - 취약점 평가 체크리스트
   - 보안 요구사항 매트릭스
   - 컴플라이언스 검증

3. **성능 최적화 템플릿**
   - 벤치마킹 가이드
   - 프로파일링 결과 분석
   - 최적화 전략 수립

4. **팀 협업 템플릿**
   - 스프린트 계획
   - 회고록 템플릿
   - 코드 리뷰 가이드

---

## 📚 관련 문서

- [옵시디언 최적화 가이드](../OBSIDIAN_OPTIMIZATION_GUIDE.md)
- [Dataview 쿼리 템플릿](dataview_queries.md)
- [AFO Kingdom 메인 문서](../AFO_KINGDOM_MAIN.md)

---

> [!tip] 템플릿 활용 팁
>
> 1. **변수 우선**: 템플릿 적용 후 즉시 필수 변수들을 채워주세요
> 2. **점진적 완성**: 모든 섹션을 한 번에 채우지 말고 우선순위에 따라 완성하세요
> 3. **링크 연결**: 관련 문서들을 적극적으로 링크하여 네트워크를 구축하세요
> 4. **정기 검토**: 생성된 문서들을 주기적으로 검토하고 업데이트하세요

---

> [!info] 템플릿 메타데이터
> **생성일**: 2025-01-27
> **버전**: 1.0.0
> **관리자**: 승상 (丞相) - AFO Kingdom
> **라이선스**: MIT
