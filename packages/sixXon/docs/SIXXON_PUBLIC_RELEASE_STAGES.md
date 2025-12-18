# SixXon 공개 단계(필터링) 로드맵 v1

**작성일**: 2025-12-13  
**목적**: “한 번에 전부 공개하지 않는다”를 문서로 고정하고, 단계별로 사람을 필터링하며(교육/기여/신뢰) 공개 범위를 확장한다.  
**SSOT**: 실제 상태/판정은 **Receipt (`logs/receipts/<id>/receipt.json` + `raw/*`)**가 단일 진실 원천이다.

---

## 0) 원칙 (변하지 않는 것)

- **Stage 0는 ‘계산기’다.** 누구나 쓸 수 있어야 한다.
- **Stage가 올라갈수록, 더 적은 사람에게 더 깊은 기능을 준다.**
- **Bridge(진실의 눈)는 오라클이다.** 공개하더라도 “조작/점수 올리기”를 허용하지 않는다.
- **브라우저/권한/네트워크 제한은 DOWN이 아니라 UNKNOWN으로 분리한다.**

---

## 1) Stage 0 — Public “계산기 / 영수증”

### 사람에게 보이는 것
- `sixxon receipt` / `sixxon status` / `sixxon explain` 같은 “상태/근거/다음 행동” 도구
- 기본 출력은 3줄(겸손 프로토콜)

### 숨기는 것
- OS(Trinity-OS) 내부 구조/전략/자동화(도구 체인) 전부
- 특정 벤더/모델에 대한 강한 의견(정치) 및 내부 용어

### 진입 조건(필터)
- 없음(누구나)

### 졸업 조건(다음 Stage로)
- Receipt를 스스로 생성/첨부하고, “말”이 아니라 “증거”로 소통할 수 있음

---

## 2) Stage 1 — Builder “수동 인증(월구독) + Wallet”

### 사람에게 보이는 것
- **월구독(웹 로그인) 기반**: “한 번 로그인 → 세션 캡처 → Wallet 암호화 저장 → CLI 재사용”
- 자동 실행은 기본 OFF(수동 open 중심)

### 문서/코드 범위
- `docs/SIXXON_AUTH_SUBSCRIPTION_FLOW.md`를 정본으로 삼는다.
- 브라우저 선택은 혼선을 막기 위해 `--browser system-chrome`로 고정한다.

### 숨기는 것
- 세션 캡처 구현 디테일(셀렉터/회피/우회)은 기본 공개 범위에서 제외

### 진입 조건(필터)
- 시크릿(세션/키)을 Git에 올리지 않는 습관이 고정됨
- `auth status`에서 `decryptable=true/false`를 이해하고 재캡처로 복구할 수 있음

### 졸업 조건
- “브라우저 난립/프릭션”을 줄이는 운영 습관(단일 브라우저 선택, 수동 open, Receipt 기반 보고)이 정착

---

## 3) Stage 2 — Contributor “MCP Tool (얇은 공개)”

### 사람에게 보이는 것
- MCP 서버를 통해 **읽기/검증 성격의 툴**을 제공한다.
- 예: Receipt 생성/검증, 환경 라벨(LOCAL/SANDBOX/CI) 판정, Health check 정렬

### 숨기는 것
- 자동 집행(권한 회수/차단/처벌) 및 내부 자동화 루프는 Stage 2에 넣지 않는다.
- 고위험 도구(삭제/마이그레이션/과금)는 기본 노출 금지(또는 ASK 강제)

### 진입 조건(필터)
- Receipt 스키마/계약을 이해하고, “증거 기반 PR”을 올릴 수 있음

---

## 4) Stage 3 — Internal “OS / Toolflow / Multi-Agent”

### 사람에게 보이는 것
- 내부 운영(Trinity-OS, Toolflow, Multi-Agent 협업)은 **원칙/계약만 공개**하고 구현/운영은 제한한다.

### 진입 조건(필터)
- SSOT(Receipt) 기반 사고가 체화되어 있고, 권한/비용/보안에 대해 스스로 멈출 수 있음
- “겸손 프로토콜(3줄)”과 “UNKNOWN 분리”를 깨지 않음

---

## 5) 관우(교육/전파)와 방통(구현)의 협업 경로

- **관우(교육/전파)**: Stage 0 문서/예제/가이드(계산기), Stage 2 공개 범위(얇은 MCP) 설계
- **방통(구현)**: Receipt/Wallet/브라우저 선택/CLI UX(3줄) 같은 “작동하는 최소 구현” 고도화

참조(현재 레포 근거):
- `docs/MULTI_AGENT_SEQUENTIAL_COLLABORATION_PLAN.md`
- `docs/SIXXON_AUTH_SUBSCRIPTION_FLOW.md`
- `docs/SIXXON_CLI_PHILOSOPHY_AND_UX.md`
