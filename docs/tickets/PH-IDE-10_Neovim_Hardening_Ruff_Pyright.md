# [PH-IDE-10] Neovim Hardening (Ruff + Pyright)

> **眞·美** - 터미널에서도 제국의 진실과 아름다움을 유지

## 📋 개요
Neovim 환경에서 Mason.nvim과 lspconfig을 활용하여 Ruff와 Pyright를 병렬로 조율하는 최적의 설정을 설계합니다.

## 🎯 목표
- `lspconfig.ruff_lsp`와 `lspconfig.pyright` 간의 충돌 방지 설정
- `conform.nvim` 또는 `none-ls`를 통한 Ruff 포매팅 우선권 부여
- 터미널 기반 고속 개발 워크플로우 지원

## 🛠️ 작업 내용
1. 가이드 문서: `docs/ide/NEOVIM_RUFF_PYRIGHT_GUIDE.md` 작성 (Lua 코드 스니펫 포함)
2. `pyproject.toml`과의 설정 동기화 검증

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: ✅ SEALED (ENFORCED)
