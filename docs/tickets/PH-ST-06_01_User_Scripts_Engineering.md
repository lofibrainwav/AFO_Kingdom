# [TICKET] PH-ST-06_01: User Scripts Engineering

## 🎯 Objective (DoD)
- [ ] Scripts 폴더(/Scripts)에 재사용 가능한 JavaScript 모듈 (`advanced_prompt.js` 등) 구축.
- [ ] Templater에서 `tp.user.script_name()` 형식을 통한 고차원 자동화 성공.
- [ ] 동적 프론트매터 생성 및 Suggester 기반 다중 선택 시스템 구현.

## 🛠️ Technical Approach
- **Modularization**: 자주 사용되는 프롬프트 및 유틸리티를 `.js` 파일로 분리.
- **tp.system integration**: `tp.system.prompt` 및 `tp.system.suggester`를 User Script 내에서 래핑하여 인지 부하 감소.
- **Dry_Run Layer**: 스크립트 실행 전 결과 미리보기 기능을 제공하여 善(Goodness) 확보.

## 🧪 Verification & Evidence
- [ ] `Scripts/advanced_prompt.js` 파일 존재 및 구문 오류 없음.
- [ ] 테스트 템플릿에서 `<% tp.user.advanced_prompt(tp) %>` 호출 시 동적 YAML 생성 확인.
- [ ] 3개 이상의 다중 선택지가 Suggester에서 정상 작동하는지 확인.

## 🛡️ Rollback Plan
- [ ] 잘못된 스크립트 파일 삭제 및 템플릿 호출 구문 제거.
