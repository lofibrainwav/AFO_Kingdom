#!/usr/bin/env python3
"""
SSOT PH-* Capsule Format Validator

Evolution Log의 SSOT/PH-* 블록들이 5줄 정규 형식 준수하는지 검증
- Status: SEALED|PARTIAL|PENDING
- Scope: [설명]
- Evidence: [증거]
- Gaps: [갭 또는 none]

사용법: python3 scripts/verify_ssot_ph_capsules.py docs/AFO_EVOLUTION_LOG.md
"""

import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("❌ 사용법: python3 scripts/verify_ssot_ph_capsules.py <evolution_log.md>", file=sys.stderr)
        sys.exit(2)

    p = Path(sys.argv[1])
    if not p.exists():
        print(f"❌ 파일 없음: {p}", file=sys.stderr)
        sys.exit(1)

    # 파일 읽기
    try:
        with open(p, encoding="utf-8") as f:
            t = f.read().splitlines()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}", file=sys.stderr)
        sys.exit(1)

    # SSOT/PH-* 헤더 찾기
    hdr = [i for i, l in enumerate(t) if re.match(r"^## \[SSOT/PH-[^]]+\]", l)]

    # 1) 캡슐 0개도 FAIL (가드가 망가진 걸 놓치지 않게)
    if not hdr:
        print("❌ No SSOT/PH-* capsules found (regex/path mismatch?)")
        print("💡 Check if the regex pattern or file path is correct")
        sys.exit(1)

    bad = []

    # 각 캡슐 검증
    for i in hdr:
        block = t[i:i+5]
        if len(block) < 5:
            bad.append((i+1, "short", ""))
            continue

        # Status 검증
        if not re.match(r"^- Status: (SEALED|PARTIAL|PENDING)$", block[1]):
            bad.append((i+1, "status", block[1]))

        # Scope 검증
        elif not re.match(r"^- Scope: .+$", block[2]):
            bad.append((i+1, "scope", block[2]))

        # Evidence 검증
        elif not re.match(r"^- Evidence: .+$", block[3]):
            bad.append((i+1, "evidence", block[3]))

        # Gaps 검증
        elif not re.match(r"^- Gaps: .+$", block[4]):
            bad.append((i+1, "gaps", block[4]))

    # 2) 실패 시 라인 번호 + 내용 표시 (수정 속도↑)
    if bad:
        print("❌ SSOT/PH-* capsule format violations:")
        for ln, why, content in bad[:10]:  # 최대 10개만
            print(f"  Line {ln}: {why}")
            if content:
                print(f"    | {content}")
        print(f"\n💡 Expected format:")
        print("  ## [SSOT/PH-XXXX/YYYY-MM-DD/<sha>] Title")
        print("  - Status: SEALED|PARTIAL|PENDING")
        print("  - Scope: [description]")
        print("  - Evidence: [evidence]")
        print("  - Gaps: [gaps or none]")
        sys.exit(1)

    print(f"✅ {len(hdr)} SSOT capsules validated (5-line format)")


if __name__ == "__main__":
    main()