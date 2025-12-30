# Visual SSOT Asset Contract (眞)

> **As-of: 2025-12-29 | Version: v1.0**
> **SSOT Principle**: "그림(SVG)은 스스로의 기원(.excalidraw)을 증명해야 한다."

## 1. Manifest Rule
- **Location**: `docs/diagrams/SSOT_VISUAL_MANIFEST.txt`
- **Format**: 
    - `#`로 시작하는 줄은 주석.
    - 빈 줄 무시.
    - 파일명은 `docs/diagrams` 기준 상대 경로.
- **Enforcement**: 매니페스트에 등록된 파일이 없거나, 등록된 파일이 실제 존재하지 않으면 CI FAIL.

## 2. Hash Stamp Rule
- **Algorithm**: SHA256 (Original `.excalidraw` file).
- **Injection**: SVG 파일 내 `<svg>` 태그 바로 다음에 삽입.
- **Format**: `<!-- SSOT-SOURCE-SHA256:<64_hex_chars> -->`
- **Enforcement**: 스탬프가 없거나, 원본 해시와 불일치할 경우 CI FAIL.

## 3. Automation Flow
1. **Source**: `.excalidraw` 편집.
2. **Export**: `.svg`로 수동 내보내기.
3. **Stamp**: `python3 scripts/stamp_visual_ssot.py` 실행.
4. **Verify**: `python3 scripts/verify_visual_sync.py` 또는 `bash scripts/public_release_prep.sh`.

---

**Trinity Score**: 眞 100% | 善 100% | 永 100%
