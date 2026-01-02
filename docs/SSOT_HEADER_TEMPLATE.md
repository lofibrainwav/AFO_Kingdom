# SSOT Header Template — AFO Kingdom Standard

```md
SSOT-HEADER
As-of: <from artifacts/.../as_of_iso8601.txt>
HEAD: <full sha from git_head.txt>
origin/main: <from origin_main_sha.txt>
Change: <one-line summary>
Evidence: <artifacts/.../>
Manifest: <artifacts/.../manifest.sha256>
Decision: AUTO_RUN | ASK_COMMANDER | BLOCK
Reproduce: <one-shot script path or inline 3-10 lines>
```

## 필드 설명

- **As-of**: ISO8601+TZ (타임존 포함)
- **HEAD**: 40자리 full SHA
- **origin/main**: SHA (로컬 ref, 네트워크 불필요)
- **Change**: 한 줄 요약
- **Evidence**: artifacts 경로
- **Manifest**: SHA256 해시 파일
- **Decision**: AUTO_RUN/ASK/BLOCK
- **Reproduce**: 재현 커맨드

## 사용법

모든 보고서 맨 위에 붙여서 사용하세요.

---

**AFO 왕국 SSOT 표준 — 영속적 기록 체계**
