# K8sStatusWidget 기본 OFF 설정 완료 보고

**날짜**: 2025-01-21  
**작업자**: 승상 (AI Agent)  
**목적**: K8sStatusWidget 기본 비활성화로 "쿠버네티스 또 뜨는" 문제 해결

---

## 배경

사용자가 "쿠버네티스 또 뜨는데" 문제를 제기했습니다. 분석 결과:

1. **GitKraken 에러**: Cursor IDE의 GitKraken 통합 기능 네트워크 문제 (코드 변경 불필요)
2. **K8sStatusWidget 문제**: 실제 K8s 클러스터 없이도 위젯이 표시되어 혼란 발생

## 해결 방안

**SSOT 원칙에 따라 환경변수로 제어**:
- 기본값: `NEXT_PUBLIC_ENABLE_K8S_WIDGET=false` (기본 OFF)
- 실제 K8s 클러스터 연결 시에만 명시적으로 `true`로 변경

## 변경 사항

### 1. 코드 변경

**파일**: `packages/dashboard/src/components/genui/K8sStatusWidget.tsx`

**변경 내용**:
```tsx
export function K8sStatusWidget() {
  // SSOT: 환경변수로 위젯 활성화 제어 (기본 OFF)
  const enabled = process.env.NEXT_PUBLIC_ENABLE_K8S_WIDGET === "true";
  if (!enabled) return null;

  return (
    <ErrorBoundary
      // ... 기존 코드 유지
```

**이유**:
- 컴포넌트 최상단에서 조기 반환으로 불필요한 렌더링 방지
- ErrorBoundary 래핑 전에 체크하여 오버헤드 최소화
- 위젯이 어디서 import되든 동일하게 동작

### 2. 환경변수 설정

**파일**: `packages/dashboard/.env.local`

**추가 내용**:
```
NEXT_PUBLIC_ENABLE_K8S_WIDGET=false
```

**참고**: `.env.local`은 `.gitignore`에 포함되어 커밋되지 않습니다.

## 검증 결과

### 코드 검증
- ✅ 환경변수 체크 로직 정상 작동
- ✅ TypeScript 타입 에러 없음 (K8sStatusWidget.tsx)
- ✅ ESLint 경고 없음 (K8sStatusWidget.tsx)

### 품질 게이트
- ✅ Lint: 경고만 존재 (기존 코드, K8sStatusWidget과 무관)
- ⚠️ Type-check: MarkdownViewer.tsx에 기존 에러 존재 (별도 이슈)

## 사용 방법

### 위젯 비활성화 (기본값)
```bash
# .env.local에 이미 설정됨
NEXT_PUBLIC_ENABLE_K8S_WIDGET=false
```

### 위젯 활성화 (실제 K8s 클러스터 연결 시)
```bash
# .env.local 수정
NEXT_PUBLIC_ENABLE_K8S_WIDGET=true
```

## GitKraken 에러 처리

**해결 방법**: Cursor 설정에서 GitKraken 통합 비활성화
- Cursor Settings → GitKraken 검색 → 통합 기능 OFF
- 또는 일시적 네트워크 문제로 무시 가능

## 완료 조건

- ✅ K8sStatusWidget 환경변수 체크 로직 추가
- ✅ .env.local에 환경변수 설정
- ✅ 코드 검증 완료
- ✅ 품질 게이트 통과 (K8sStatusWidget 관련)
- ✅ 문서 작성 완료

## 향후 작업

1. 실제 K8s 클러스터 연결 시 환경변수만 `true`로 변경
2. 필요 시 실제 K8s API 연결 로직 추가 (현재는 더미 데이터)

---

**SSOT 원칙 준수**: 환경변수로 명시적 제어, 추측 기반 로직 없음

