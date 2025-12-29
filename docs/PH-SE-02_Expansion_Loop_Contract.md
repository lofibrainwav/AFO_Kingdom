# PH-SE-02: Expansion Loop Contract + Ticket Format SSOT

**자율적 확장 루프 자동 생성 티켓**

## 목표
Expansion Loop의 Contract와 Ticket Format을 SSOT로 표준화하여 재현성과 감사 가능성을 100% 확보

## 현재 상태 분석
- PH-SE-01 완료: 기본 확장 루프 구축
- Trinity Score: 1.0 (건강)
- 확장 루프: 안전하게 작동 중

## 실행 계획
1. 티켓 포맷 표준화 (ID/파일/내용 구조)
2. 산출물 구조 표준화 (artifacts/expansion/)
3. 실행 결과 포맷 표준화 (run.json)
4. DRY_RUN 모드 구현
5. Contract 검증 로직 추가

## 완료 기준
- 티켓 파일 포맷: `artifacts/expansion/<date>/tickets/<id>.md`
- 티켓 ID 규칙: `PH-SE-02-001` 형태 (충돌 방지)
- 실행 결과: `artifacts/expansion/<date>/run.json`
- 필수 섹션: "실행/검증/회고" (없으면 FAIL)
- DRY_RUN 지원: 티켓 생성만 수행

## Contract 세부 사항

### 1. 티켓 파일 포맷 (표준화)
```markdown
# <TICKET_ID>: <TITLE>

**생성 시각**: <ISO_TIMESTAMP>
**확장 루프**: 자동 생성
**우선순위**: <PRIORITY>

## 목표
<OBJECTIVE>

## 현재 상태 분석
<ANALYSIS>

## 실행 계획
<PLAN>

## 완료 기준
<COMPLETION_CRITERIA>

## 상태
🚀 진행 중 (자율적 확장 루프 자동 생성됨)
```

### 2. 티켓 ID 규칙
- 형식: `PH-SE-<PHASE>-<SEQUENTIAL_NUMBER>`
- 예시: `PH-SE-02-001`, `PH-SE-02-002`
- 충돌 방지: 동일 날짜 내 시퀀셜 넘버링

### 3. 산출물 구조
```
artifacts/expansion/
├── <date>/
│   ├── tickets/
│   │   ├── PH-SE-02-001.md
│   │   └── PH-SE-02-002.md
│   └── run.json
```

### 4. 실행 결과 포맷 (run.json)
```json
{
  "run_id": "<timestamp>",
  "tickets_generated": 2,
  "tickets_executed": 2,
  "success_count": 2,
  "failure_count": 0,
  "total_runtime_seconds": 45,
  "tickets": [
    {
      "id": "PH-SE-02-001",
      "status": "completed",
      "runtime_seconds": 12,
      "result": "success"
    }
  ]
}
```

### 5. 필수 섹션 검증
모든 티켓은 다음 섹션을 반드시 포함해야 함:
- 실행 계획 (실행)
- 완료 기준 (검증)
- 결과 요약 (회고)

## 구현 세부 사항

### DRY_RUN 모드
```bash
DRY_RUN=true ./scripts/run_expansion_loop.sh
# 티켓 생성만 수행, 실제 실행 생략
```

### Contract 검증
```bash
./scripts/validate_expansion_contract.sh <ticket_file>
# 티켓 포맷 준수 여부 검증
```

## 구현 결과
- 티켓 ID 규칙 PH-SE-02-001 구현 완료
- 산출물 구조 artifacts/expansion/<date>/tickets/ 생성
- run.json 포맷 표준화 및 생성 로직 구현
- DRY_RUN 모드 및 필수 섹션 검증 추가
- Contract 준수 테스트 완료 (DRY_RUN 성공)

## 상태
✅ 완료 (Expansion Loop Contract SSOT 구축)
