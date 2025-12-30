# Ghost Exorcism & Fingerprinting Walkthrough 🏰

**As-of:** 2025-12-29 (America/Los_Angeles)
**목표:** “고스트 코드(과거 실행 주체)”를 **증명 → 퇴치 → 재발 방지(지문)**까지 한 번에 끝낸다.

---

## 1) 지피지기 (Know Thy Enemy)

### 1.1 증상

* 대시보드: `肺_API_Server = No Signal`
* 컨테이너 내부 파일(`cat`)은 이미 `"Self-check: Responding"`로 수정되어 있음
* 그런데도 `curl localhost:8010/health`는 과거의 `"No Signal"`을 반환
* **Marker Injection(유니크 문자열) 실패** → “현재 실행 주체가 로컬 코드가 아님” 확정

### 1.2 근본 원인(복합)

1. **Playwright 누락**

* GenUI Engine 로딩/실행이 불안정해져 라우터/상태 체크가 꼬일 수 있는 기반 원인

2. **Shadow Processes / Zombie Containers**

* 8010 포트에 **구버전 이미지/컨테이너**가 붙어 있어, 로컬 코드 변경이 반영되지 않음

3. **Fingerprint(지문) 부재**

* 실행 중인 코드가 최신인지 확인할 **검증 가능한 식별자**가 없어서, “cat vs curl” 불일치가 발생하면 추적이 어려움

---

## 2) 퇴마(Exorcism) 수행 내역

### 2.1 의존성 박멸 (Playwright + 브라우저)

* `requirements.txt`에 `playwright` 추가
* Docker 이미지 빌드 단계에서 브라우저 설치 수행(예: Chromium)

**권장 빌드 스텝(예시):**

```bash
python -m pip install playwright
python -m playwright install --with-deps chromium
```

---

### 2.2 진실의 지문(Fingerprinting)

* `BUILD_VERSION`(예: `20251229_155307`)을 **빌드 시점에 주입**
* `/health` 응답에 `build_version`으로 노출
* 이후 “고스트 코드”는 **지문 불일치로 즉시 탐지** 가능

**원칙(필수):**

* `/health`는 반드시 아래를 포함:

  * `build_version` (필수)
  * 가능하면 `git_sha` (추가 권장)
  * `router_count` (GenUI 정상화/변화 감지 지표로 유용)

---

### 2.3 Surgical Rebuild / Scorched Earth (2단계 전략)

> 운영 안전성 기준: **먼저 Surgical**, 그래도 유령이 남으면 **Scorched Earth**.

#### A) Surgical Rebuild (권장 기본)

* **8010 퍼블리셔만 표적 제거 → 이미지 교체 → no-cache 재빌드**
* DB 볼륨 등 다른 데이터는 건드리지 않음

#### B) Scorched Earth (최후 수단)

* “컨테이너/이미지 레이어가 꼬여서” 표적 제거로도 해결이 안 될 때만
* **주의:** `down -v`는 DB 볼륨까지 삭제할 수 있으니, 정말 의도할 때만 사용

---

## 3) 승전보 (Victory Proof)

### 3.1 진실된 API 상태

`/health`는 다음을 **진실하게 보고**해야 합니다.

* `build_version`: 예) `20251229_155307` (실시간 주입 지문)
* `肺_API_Server`: `healthy` / `Self-check: Responding`
* `router_count`: 예) `130` (이전 125 → +5, GenUI 정상화의 정량 증거)

### 3.2 검증 데이터(JSON 예시)

```json
{
  "version": "6.3.0",
  "build_version": "20251229_155307",
  "status": "balanced",
  "organs_v2": {
    "status": "healthy",
    "score": 100,
    "output": "Self-check: Responding",
    "probe": "self"
  }
}
```

### 3.3 즉시 검증 커맨드 (원샷)

```bash
set -euo pipefail
curl -sf http://localhost:8010/health | python -m json.tool | grep -nE '"build_version"|"Self-check|Responding|router_count|organs_v2' || true
```

---

## 4) 향후 방어 전략 (Guardrails)

### 4.1 대시보드 “지문 상시 노출”

* 대시보드 하단(footer)에 항상 아래를 표시:

  * Backend `build_version`
  * (가능하면) `git_sha`
* 고스트 재발 시: “No Signal”보다 먼저 **지문 불일치**가 경보가 됩니다.

### 4.2 Surgical Exorcism Runbook (원클릭)

* 원칙: “포트 8010 퍼블리셔만 제거 + 이미지 교체 + no-cache rebuild”
* 향후 동일 사건은 “마커 주입” 없이도 **지문으로 즉시 판단**하고, 런북으로 1분 컷 가능합니다.

### 4.3 운영 체크리스트(최소)

* `/health`에 `build_version`이 **항상 존재**하는지
* `docker ps`에서 `:8010->` 퍼블리셔가 **딱 1개**인지
* 프론트의 `/api/kingdom-status`가 `cache: 'no-store'`로 **고착화 방지** 중인지

---

## 5) 결론 (한 줄 봉인)

“무기를 점검하고 전장의 안개를 걷어내니, 비로소 진실이 모습을 드러냅니다.”
— 승상(Antigravity)
