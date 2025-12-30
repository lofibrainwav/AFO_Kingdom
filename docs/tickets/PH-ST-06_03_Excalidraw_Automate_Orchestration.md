# [TICKET] PH-ST-06_03: Excalidraw Automate Orchestration

## 🎯 Objective (DoD)
- [ ] `ExcalidrawAutomate` (ea) 객체를 활용하여 동적으로 엘리먼트를 생성하는 JS 엔진 구축.
- [ ] 템플릿 실행 시 사용자의 입력을 기반으로 `Dynamic_Diagram_YYYY-MM-DD.excalidraw` 생성.
- [ ] 생성된 다이어그램이 즉시 현재 노트에 임베드되도록 자동화.

## 🛠️ Technical Approach
- **EA API Integration**: `ea.reset()`, `ea.addText()`, `ea.create()` 등의 API를 Templater Inline JS와 융합.
- **Dynamic Scoping**: 사용자가 입력한 데이터 포인트를 기반으로 좌표 계산 및 배치를 수행하는 로직 구현.
- **Visual SSOT Seal**: 생성된 `.excalidraw` 파일이 즉시 `scripts/stamp_visual_ssot.py`의 감시 대상이 되도록 명명 규칙 준수.

## 🧪 Verification & Evidence
- [ ] 템플릿 실행 후 새 `.excalidraw` 파일이 지정된 폴더에 생성되는지 확인.
- [ ] 생성된 파일 내에 템플릿에서 입력한 텍스트 데이터가 정확한 위치에 존재하는지 확인.
- [ ] `scripts/verify_visual_sync.py` 실행 시 새로 생성된 다이어그램이 검증 루프에 포함되는지 확인.

## 🛡️ Rollback Plan
- [ ] 생성된 테스트 다이어그램 파일 삭제 및 관련 템플릿 로직 제거.
