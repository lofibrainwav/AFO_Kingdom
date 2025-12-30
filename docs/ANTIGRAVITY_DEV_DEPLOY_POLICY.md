# Antigravity Dev Deploy Policy

## AUTO_DEPLOY=True + DRY_RUN_DEFAULT=True 조합 정책

### 정책 개요

**dev 환경에서 AUTO_DEPLOY=True + DRY_RUN_DEFAULT=True** 조합은 다음과 같은 의미를 가진다:

- **AUTO_DEPLOY=True**: 자동 실행 트리거 활성화 (형님 승인 시 즉시 실행 가능)
- **DRY_RUN_DEFAULT=True**: 기본적으로 모든 위험 동작을 시뮬레이션 (안전 우선)

### 조합 의미

이 조합은 **"준비된 상태에서 안전하게 테스트"** 모드를 의미한다:

1. **준비 상태 표시**: 시스템이 자동 실행 준비가 되었음을 표시
2. **안전 실행 강제**: 실제로는 DRY_RUN으로 모든 변경을 시뮬레이션
3. **형님 승인 대기**: Trinity Score 기반 ASK_COMMANDER 모드에서 형님 승인 기다림

### dev 환경 적용 사례

```json
{
  "ENVIRONMENT": "dev",
  "AUTO_DEPLOY": true,
  "DRY_RUN_DEFAULT": true,
  "meaning": "자동 실행 준비 완료, 안전 모드로 테스트 중"
}
```

### prod 환경 대비

| 환경 | AUTO_DEPLOY | DRY_RUN_DEFAULT | 의미 |
|------|-------------|----------------|------|
| **dev** | `true` | `true` | 준비 상태 + 안전 실행 |
| **prod** | `true` | `false` | 실제 자동 실행 |
| **staging** | `false` | `true` | 수동 승인 + 안전 실행 |

### 정책 준수 사항

- **SSOT**: 이 조합은 dev 환경에서만 허용
- **감사**: 모든 실행은 증거 로그(`artifacts/antigravity/`)에 기록
- **안전**: DRY_RUN으로 실제 변경 방지
- **투명**: 형님 승인 없이 자동 실행 불가

### 관련 문서

- [Antigravity System Status](./ANTIGRAVITY_SYSTEM_STATUS.md)
- [AFO Chancellor Graph Spec](./AFO_CHANCELLOR_GRAPH_SPEC.md)
- 봉인 증거: `artifacts/antigravity/20251230_132055/`

---

**봉인일**: 2025-12-30
**정책 승인**: Commander (형님)
**SSOT 태그**: `antigravity-seal-2025-12-30`
