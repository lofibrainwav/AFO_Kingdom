# [PH-ST-06] Obsidian Deployment Automation (Golden Path)

> **眞善美孝永** - Obsidian 환경 배포 자동화 및 정합성 강제화

## 📋 개요
Obsidian Vault의 Scripts 및 Templates 자산을 저장소(Repo)와 동기화하고, Templater 설정의 경로 정합성을 자동으로 패치하는 통합 배포 스크립트를 구축합니다.

## 🎯 목표
- Repo의 `docs/Scripts` 및 `docs/_templates` 자산을 Vault의 `Scripts`, `Templates` 폴더로 통합 배포
- `templater.json` 설정의 경로(`user_scripts_folder`, `templates_folder`)를 신규 구조에 맞게 자동 패치
- 백업 및 롤백 메커니즘 제공으로 안정성(善) 확보

## 🛠️ 작업 내용

### 1. 통합 배포 스크립트 작성
- **파일**: `scripts/obsidian_deploy_golden_path.sh`
- **기능**:
    1. **Validation**: Repo 내 자산 존재 여부 확인
    2. **Backup**: 대상 Vault 전체 백업 생성
    3. **Injection**: `Scripts`, `Templates` 폴더 주입 및 미러링
    4. **Patching**: `templater.json` 경로 문자열 자동 치환 (Python 활용)
    5. **Verification**: 배치 후 구조 및 설정 파일 존재 확인

### 2. 스크립트 고도화 (眞/美)
- 구형 경로(`_templates/scripts`)와 신규 경로(`Scripts`) 간의 과도기적 호환성을 위해 미러링 로직 포함
- Obsidian 플러그인 바이너리 설치 상태 점검 도구 포함

## ✅ 성공 기준
- `bash scripts/obsidian_deploy_golden_path.sh` 실행 시 백업 생성 및 자산 주입 완료
- Vault 내 `templater.json`의 경로가 `Scripts` 및 `Templates`로 자동 변경됨
- Obsidian 앱 내에서 템플릿 실행 시 스크립트 로드 오류가 발생하지 않음

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: 🔴 OPEN (READY FOR EXECUTION)
