# [PH-IDE-09] VSCode Hardening (Ruff + Pyright + Async Debug)

> **美·孝** - 사령관님의 개발 워크플로우를 우아하고 평온하게 고도화

## 📋 개요
VSCode 환경에서 Ruff(린팅/포매팅)와 Pyright(타입 체킹)를 완벽하게 통합하고, 특히 비동기(Async) 코드 디버깅 효율을 극대화하기 위한 설정을 주입합니다.

## 🎯 목표
- `.vscode/settings.json`을 통한 Ruff + Pyright(Pylance) 연동
- `.vscode/launch.json`을 통한 고급 비동기 디버깅 환경 구축
- 실시간 피드백 루프 완성 (Trinity Score 상승)

## 🛠️ 작업 내용
1. `settings.json`: Ruff LSP(nativeServer) 활성화 및 Pylance 타입 체킹 모드 동기화
2. `launch.json`: `AFO Core Debug` 및 `Attach to FastAPI` 비동기 최적화 프로파일 추가
3. 가이드 문서: `docs/ide/VSCODE_RUFF_PYRIGHT_DEBUG_GUIDE.md` 작성

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: ✅ SEALED (ENFORCED)
