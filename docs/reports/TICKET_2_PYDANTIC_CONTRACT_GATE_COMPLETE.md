# 티켓 2: Pydantic Contract Gate 추가 완료

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7 + 지피지기

---

## ✅ 완료된 작업

### 1. 기존 작업 확인 (지피지기)
- ✅ `generate_widgets_from_html.mjs` 존재 확인
- ✅ `widgets.generated.json` 생성됨 (35개 위젯)
- ✅ `registry.ts`에 generated widgets 자동 등록 추가됨

### 2. Pydantic v2 모델 생성
- ✅ `packages/afo-core/models/widget_spec.py` 생성
  - `BaseWidgetSpec`: 기본 위젯 스펙
  - `GeneratedWidgetSpec`: HTML에서 생성된 위젯
  - `ManualWidgetSpec`: 수동 등록 위젯
  - `ApiWidgetSpec`: API 생성 위젯
  - `WidgetSpecFlexible`: 실제 JSON 구조를 수용하는 유연한 모델
  - `WidgetsPayloadFlexible`: 위젯 목록 컨테이너

### 3. 검증 스크립트 생성
- ✅ `scripts/validate_widgets_json.py` 생성
  - `widgets.generated.json` 읽기
  - Pydantic v2로 검증
  - 중복 ID 체크
  - 에러 시 exit code 1

### 4. 검증 실행
- ✅ 검증 스크립트 실행 성공
- ✅ 35개 위젯 검증 통과
- ✅ 중복 ID 없음 확인

---

## 📊 생성된 파일

1. `packages/afo-core/models/widget_spec.py` - Pydantic v2 모델
2. `scripts/validate_widgets_json.py` - 검증 스크립트

---

## 🔧 설계 원칙

### Pydantic은 "Contract Gate"로만 사용
- ❌ 프론트엔드 빌드 경로에 포함하지 않음
- ✅ 백엔드/CI에서만 검증
- ✅ 선택적 FastAPI 엔드포인트에서 사용 가능

### Node 파서 흐름 유지
- ✅ `generate_widgets_from_html.mjs`는 그대로 유지
- ✅ `widgets.generated.json` 생성은 Node로 처리
- ✅ Pydantic은 생성된 JSON을 검증만 함

---

## 🎯 사용 방법

### 로컬 검증
```bash
python3 scripts/validate_widgets_json.py
```

### CI 통합 (선택적)
```yaml
- name: Validate widgets.json
  run: python3 scripts/validate_widgets_json.py
```

### FastAPI 엔드포인트 (선택적)
```python
from models.widget_spec import WidgetsPayloadFlexible

@app.get("/api/widgets/validate")
async def validate_widgets():
    payload = WidgetsPayloadFlexible.model_validate_json(
        widgets_json_path.read_text()
    )
    return {"valid": True, "count": payload.count}
```

---

## 📋 다음 단계

티켓 3: HTML 추출 및 React 렌더
- 각 위젯의 HTML 조각(innerHTML) 저장
- 빌드 타임에 섹션별 HTML fragment 파일 생성
- `/docs/[slug]`에서 fragment 렌더
- React 위젯이 있으면 override(교체)

---

**상태**: 티켓 2 + Pydantic Contract Gate 완료. 백엔드/CI에서만 검증하는 구조로 완성.

