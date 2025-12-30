# [TICKET] PH-ST-06_02: Reactive Hooks & Dataview Sync

## 🎯 Objective (DoD)
- [ ] `tp.hooks.on_all_templates_executed`를 활용한 동기화 루프 구현.
- [ ] 템플릿 실행 즉시 Dataview 테이블 및 메타데이터 캐시가 100% 일치하도록 보장.
- [ ] 모든 비동기 Hook에 `Try/Catch + Notice` 에러 핸들링 패턴 적용.

## 🛠️ Technical Approach
- **Event Lifecycle**: 템플릿 텍스트 삽입 완료 후 발동되는 Hook 레이어 사용.
- **Metadata Cache Resolve**: `app.metadataCache.resolve`를 호출하여 Obsidian 색인 지연 문제(Race Condition) 방지.
- **Async Robustness**: `Promise.allSettled` 패턴을 사용하여 부분적 실패가 전체 자동화를 중단하지 않도록 설계.

## 🧪 Verification & Evidence
- [ ] 템플릿 실행 후 Dataview 리프레시 성고 메타데이터 캐시 대기 확인 (Notice 알림).
- [ ] 의도적 에러 유발 시 사용자에게 경고(Notice)와 Fallback 메시지 출력 여부 확인.
- [ ] 실시간으로 변경된 프론트매터 값이 Dataview 쿼리에 즉각 반영되는지 확인.

## 🛡️ Rollback Plan
- [ ] 템플릿 파일 내 `<%* ... %>` 블록 내의 Hook 등록 코드 제거.
