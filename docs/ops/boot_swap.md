# Boot-Swap (Reflexive Learning Profile) — Ops Guide

## 목적
런타임 시작 시 learning profile(JSON)을 로드???면 항상 기본값(SSOT)?ble / Disable
- Enable: AFO_LEAR- EnabROFILE_PATH=/abs/or/rel/path.json
- Disable: unset AFO_LEARNING_PROFILE_PATH

## Health
GET /chancellor/learning/health
- status: applied | fallback | disabled
- effective_config: 실제 적용된 weights/thresholds
- applied_overrides: 반영된 필드 목록
- errors: 실패 사유 목록
- sha256/source_path/loaded_at/version

## Validation Rules (권장)
- weights: 모든 값 0~1, 합 1.0(허용오차 EPS)
- thresholds: 0~100 범위
- 기본 정책: safety 완화 금지
  - auto_run_trinity < base => reject
  - auto_run_risk > base => reject
  - 예외: AFO_LEARNING_ALLOW_WEAKEN_SAFETY=1

## Seal (Evidence)
scripts/seal_boot_swap.sh 실행 시
- learning_health_*.json
- 5pillars_*.json
- health_*.json
를 artEARNING_BOOT_SWAP=0 같은 킬스위 ??? 가능
