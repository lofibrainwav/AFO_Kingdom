# SSOT Verification Template (표준화 템플릿)

## 목적
모든 작업 완료 시 이 템플릿을 사용하여 SSOT 기반 검증을 수행합니다.

## 템플릿 구조

```bash
#!/bin/bash
# SSOT Verification Script (작업명) v1.2.x
# Evidence-based validation with no sensitive data exposure

# Anchor & As-of (SSOT Required)
echo "AS_OF: $(date -u +%Y-%m-%dT%H:%M:%S%z)"
echo "ANCHOR: $(git rev-parse --abbrev-ref HEAD) | $(git rev-parse HEAD)"
echo "RUNTIME: ONLINE"
echo ""

# Pass Rules (SSOT Required - 작업별 정의)
echo "RULE: [작업별 PASS 기준 1]"
echo "RULE: [작업별 PASS 기준 2]"
echo ""

# Evidence Block (Commands → Outputs)
echo "## Evidence (Commands → Outputs)"
echo ""

echo "1) [검증 항목 1]"
echo "- Command: [실행할 명령어]"
echo "- Output: $([명령어 실행])"
echo "- Pass rule: [PASS 조건]"
echo ""

echo "2) [검증 항목 2]"
echo "- Command: [실행할 명령어]"
echo "- Output: $([명령어 실행])"
echo "- Pass rule: [PASS 조건]"
echo ""

# Trinity score (항상 포함)
echo "N) Trinity score"
echo "- Command: grep -c 'trinity_score' docs/ssot/traces/traces.jsonl 2>/dev/null || echo 'TRINITY: N/A'"
trinity_check=$(grep -c 'trinity_score' docs/ssot/traces/traces.jsonl 2>/dev/null || echo "0")
if [ "$trinity_check" = "0" ]; then
    echo "- Output: TRINITY: N/A (no trace key)"
else
    echo "- Output: $(grep -c 'trinity_score' docs/ssot/traces/traces.jsonl)"
fi
echo "- Pass rule: If missing → Trinity=N/A"
echo ""

# Exit Code (SSOT Required)
echo "EXIT_CODE=$?"
```

## 적용 방법

### 1. 작업 시작 전
- 이 템플릿을 복사하여 작업명에 맞게 수정
- `scripts/verify_[작업명].sh`로 저장

### 2. 작업 완료 후
- 스크립트 실행: `./scripts/verify_[작업명].sh`
- 결과가 모두 PASS인지 확인
- `EXIT_CODE=0`인지 확인

### 3. 문서화
- 워크숍 문서에 SSOT Evidence 블록 추가:

```md
## SSOT Verification ([작업명]) — Evidence

- As-of: [타임스탬프]
- Repo Anchor: [브랜치 | 해시]
- Runtime: ONLINE
- Trinity: [Reality]=[값] | [Target (Simulation)]=[값]

### Evidence (Commands → Outputs)

1) [항목명]
- Command: [명령어]
- Output: [결과]
- Pass rule: [조건]
```

## 검증 원칙

1. **증거 기반**: 모든 주장은 Command + Output으로 증명
2. **민감 데이터 보호**: 절대 민감 정보 노출 금지
3. **재현성**: 언제든지 동일한 결과 나와야 함
4. **완전성**: EXIT_CODE=0로 끝나야 함

## 예시: 보안 정리 작업

```bash
#!/bin/bash
# SSOT Verification Script (Security/Cleanup) v1.2.x

echo "AS_OF: $(date -u +%Y-%m-%dT%H:%M:%S%z)"
echo "ANCHOR: $(git rev-parse --abbrev-ref HEAD) | $(git rev-parse HEAD)"
echo "RUNTIME: ONLINE"
echo ""

echo "RULE: sensitive_cache_count must be 0"
echo "RULE: .gitignore must include .mypy_cache patterns"
echo ""

echo "## Evidence (Commands → Outputs)"
echo ""

echo "1) Sensitive cache files count"
echo "- Command: find . -path '*/.mypy_cache*' -name '*secrets*' -type f | wc -l | tr -d ' '"
echo "- Output: $(find . -path '*/.mypy_cache*' -name '*secrets*' -type f | wc -l | tr -d ' ')"
echo "- Pass rule: output == 0"
echo ""

echo "EXIT_CODE=$?"
```

## 자동화 적용

CI/CD에 통합하여 모든 PR에서 자동 검증:

```yaml
- name: SSOT Verification
  run: |
    bash scripts/verify_[작업명].sh > ssot_output.txt
    if ! grep -q "EXIT_CODE=0" ssot_output.txt; then
      echo "SSOT verification failed"
      exit 1
    fi
```

이 템플릿을 사용하여 앞으로 모든 작업에서 SSOT 기반 검증을 표준화합니다.