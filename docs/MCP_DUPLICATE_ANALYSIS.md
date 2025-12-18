# MCP 설정 중복 분석 및 정리

## 🔍 발견된 중복 항목

### 1. `read_file` 도구 중복

**중복 위치**:
- ✅ `filesystem` (외부 MCP 서버) - 표준 파일 시스템 접근
- ⚠️ `afo-ultimate-mcp` - read_file 도구
- ⚠️ `afo-skills-mcp` - read_file 도구

**문제점**:
- 같은 기능의 도구가 3곳에 존재
- 사용자가 어떤 것을 사용해야 할지 혼란

**해결 방안**:
- `afo-skills-mcp`에서 `read_file` 제거 (afo-ultimate-mcp에 있으므로)
- `filesystem` 서버는 표준 서버이므로 유지
- 역할 분담:
  - `filesystem`: 표준 파일 시스템 접근 (외부 서버)
  - `afo-ultimate-mcp`: AFO 전용 파일 작업 + Trinity Score

---

### 2. 파일 시스템 접근 중복

**중복 위치**:
- `filesystem` 서버: 표준 파일 시스템 접근
- `afo-ultimate-mcp`: read_file, write_file

**해결 방안**:
- `filesystem` 서버는 표준이므로 유지
- `afo-ultimate-mcp`는 AFO 전용 기능 + Trinity Score 제공으로 역할 구분

---

### 3. Trinity Score 계산 중복 가능성

**중복 위치**:
- `trinity-score-mcp`: Trinity Score 계산 서버
- `calculate_trinity_score` skill: API 엔드포인트

**분석**:
- `trinity-score-mcp`: MCP 프로토콜 기반 계산
- `calculate_trinity_score`: HTTP API 기반 계산
- **중복 아님**: 다른 인터페이스이므로 둘 다 유지

---

## ✅ 정리 방안

### 1. `afo-skills-mcp`에서 `read_file` 제거

**이유**:
- `afo-ultimate-mcp`에 이미 존재
- `afo-skills-mcp`는 CuPy 가속 및 사실 검증에 집중해야 함

**변경 후 도구**:
- `cupy_weighted_sum`: GPU 가속 가중 합 계산
- `verify_fact`: 사실 검증 (Hallucination Defense)

---

### 2. 역할 명확화

#### `filesystem` (외부)
- **역할**: 표준 파일 시스템 접근
- **특징**: 범용적, 표준 MCP 서버

#### `afo-ultimate-mcp`
- **역할**: AFO 전용 파일 작업 + 시스템 명령
- **특징**: Trinity Score 자동 계산
- **도구**: shell_execute, read_file, write_file, kingdom_health

#### `afo-skills-mcp`
- **역할**: 고성능 계산 + 사실 검증
- **특징**: CuPy GPU 가속, Trinity Score 자동 계산
- **도구**: cupy_weighted_sum, verify_fact

---

## 📋 정리 후 구조

### MCP 서버 역할 분담

1. **외부 표준 서버** (5개)
   - `memory`: 지식 그래프
   - `filesystem`: 표준 파일 시스템
   - `sequential-thinking`: 단계별 추론
   - `brave-search`: 웹 검색
   - `context7`: 라이브러리 문서

2. **AFO 전용 서버** (3개)
   - `afo-ultimate-mcp`: 범용 도구 (파일, 명령, 건강 체크)
   - `afo-skills-mcp`: 고성능 계산 + 사실 검증
   - `trinity-score-mcp`: Trinity Score 계산

---

## 🎯 권장 사항

1. **파일 읽기/쓰기**: `afo-ultimate-mcp` 사용 (Trinity Score 포함)
2. **표준 파일 접근**: `filesystem` 사용 (범용)
3. **GPU 가속 계산**: `afo-skills-mcp` 사용
4. **Trinity Score 계산**: `trinity-score-mcp` 또는 `calculate_trinity_score` skill 사용

