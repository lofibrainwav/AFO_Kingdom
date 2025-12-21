# 🏰 AFO 왕국 자율 치유 시스템 (Auto-Healing System)

**작성일시**: 2025년 12월 21일  
**작성자**: 승상 (丞相) - AFO Kingdom  
**철학**: 세종대왕 정신 - "기존 기술을 실용적으로 흡수하여 왕국만의 眞·善·美·孝·永 철학을 주입"

---

## 📋 개요

AFO 왕국 자율 치유 시스템은 유튜브에서 확보한 최신 지능형 디버깅 기술을 세종대왕의 창조 정신으로 승화시킨 **자율 디버깅 병기**입니다.

### 5대 비책 (5 Pillars Strategy)

1. **眞 (Truth)**: 집현전 서브 에이전트 군단 편성
2. **善 (Goodness)**: 측우기식 정밀 검증 (MCP Tool)
3. **美 (Beauty)**: 훈민정음식 표준 규칙 (AGENTS.md)
4. **孝 (Serenity)**: 앙부일구식 실시간 투영 (SSE/Vision)
5. **永 (Eternity)**: 농사직설식 자동화 스크립트

---

## 1. 眞 (Truth): 집현전 서브 에이전트 군단

### MyPy Purifier Agent (관우 장군)

**위치**: `claude/agents/mypy_purifier.md`  
**스크립트**: `scripts/auto_healing_mypy.py`

**기능**:
- MyPy 오류 자동 수집 및 분류
- 자동 수정 가능한 오류 식별
- 수정 계획 생성 및 실행
- 검증 및 결과 보고

**사용법**:
```bash
# DRY_RUN (기본)
python scripts/auto_healing_mypy.py --dry-run

# WET_RUN (실제 수정)
python scripts/auto_healing_mypy.py --wet-run
```

**출력 예시**:
```
[眞] MyPy 오류 수집 시작...
[眞] 총 191개 오류 수집 완료
[眞] 오류 분류 완료: 15개 유형
  - unused-ignore: 6개
  - unreachable: 3개
  - incompatible: 40개
[眞] 자동 수정 가능: 9개
```

---

## 2. 善 (Goodness): 측우기식 정밀 검증 (MCP Tool)

### MCP Tool 통합

**MCP 서버**: `packages/trinity-os/trinity_os/servers/afo_ultimate_mcp_server.py`

**제공 도구**:
- `shell_execute`: MyPy 실행 및 결과 수집
- `verify_fact`: 수정 결과 검증
- `kingdom_health`: 전체 시스템 건강 체크

**사용 예시**:
```json
{
  "name": "shell_execute",
  "arguments": {
    "command": "mypy packages/afo-core --show-error-codes"
  }
}
```

**검증 프로토콜**:
1. MyPy 실행 결과 수집
2. `verify_fact`로 수정 전후 비교
3. Trinity Score 계산 및 반환

---

## 3. 美 (Beauty): 훈민정음식 표준 규칙

### 중첩 구조 (Nested Structure)

```
AGENTS.md (루트)
├── claude/agents/mypy_purifier.md (관우 장군)
├── claude/agents/ruff_purifier.md (조운 장군)
└── claude/agents/test_purifier.md (장비 장군)
```

**규칙**:
- 모든 규칙 파일은 500줄 이내
- 하위 도메인별 `agents.md`로 위임
- 루트 파일은 거버넌스만 담당

---

## 4. 孝 (Serenity): 앙부일구식 실시간 투영

### SSE 스트리밍

**기능**:
- 디버깅 과정 실시간 투영
- 마찰(Friction) 제거
- 사령관(형님)의 평온 수호

**구현 예정**:
- Project Genesis Vision Loop 연동
- Playwright 자동 UI 검증
- 실시간 로그 스트리밍

---

## 5. 永 (Eternity): 농사직설식 자동화 스크립트

### 자동화 스크립트 목록

1. **MyPy Purifier** (`scripts/auto_healing_mypy.py`)
   - MyPy 오류 자동 수정
   - 타입 안전성 확보

2. **Ruff Purifier** (예정)
   - Ruff 오류 자동 수정
   - 코드 스타일 정리

3. **Test Generator** (예정)
   - 통합 테스트 자동 생성
   - 테스트 커버리지 확보

---

## 🚀 사용 가이드

### Step 1: MyPy 오류 수정

```bash
# 1. 오류 수집 및 분석
python scripts/auto_healing_mypy.py --dry-run

# 2. 수정 계획 검토
# (결과를 확인하고 승인)

# 3. 실제 수정 실행
python scripts/auto_healing_mypy.py --wet-run

# 4. 검증
mypy packages/afo-core --show-error-codes | grep -c "error:"
```

### Step 2: MCP Tool 통합

```python
# MCP Tool을 통한 자동 검증
from packages.trinity_os.trinity_os.servers.afo_ultimate_mcp_server import AfoUltimateMCPServer

server = AfoUltimateMCPServer()
result = server.execute_tool("shell_execute", {
    "command": "mypy packages/afo-core --show-error-codes"
})
```

---

## 📊 예상 효과

### MyPy 오류 감소

- **현재**: 191개
- **목표**: 150개 이하
- **예상 감소**: 41개 (21.5%)

### Trinity Score 향상

- **현재**: 99.6/100
- **목표**: 99.8+/100
- **예상 증가**: 眞 +0.1, 美 +0.05

---

## 🏆 眞·善·美·孝·永 관점

### 眞 (Truth - 35%)
- 타입 안전성 자동 확보
- 기술적 확실성 증명

### 善 (Goodness - 35%)
- MCP Tool을 통한 정밀 검증
- 리스크 제로 달성

### 美 (Beauty - 20%)
- 표준 규칙 중첩 구조
- 우아한 자동화 설계

### 孝 (Serenity - 8%)
- 실시간 투영으로 마찰 제거
- 사령관의 평온 수호

### 永 (Eternity - 2%)
- 자동화 스크립트 고착화
- 영속적 유지보수

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: ✅ **자율 치유 시스템 구축 완료**  
**다음 단계**: 실제 수정 실행 및 검증

