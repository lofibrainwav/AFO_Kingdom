## 🏛️ Recommended Standard: Option B+ (Hybrid-Sync + Hash Stamp)
**원본(`.excalidraw`)과 렌더(`.svg`)를 함께 관리하되 해시 스탬프로 동기화 강제.**

- **Source**: `.excalidraw` (진실)와 `.svg` (보기)를 한 쌍으로 커밋.
- **Sync Mechanism**: `.svg` 파일 내부에 원본의 SHA256 해시를 주석으로 포함.
- **포털 연결**: Master Index 및 Obsidian은 `.svg`를 임베드하여 어디서나 즉시 확인 가능.
- **Pros**:
    - **眞 (Truth)**: OS 시간(mtime)과 상관없이 "내보내기 누락" 100% 감지.
    - **孝 (Serenity)**: CI에 무거운 렌더러(Headless Browser 등) 설치 불필요.
    - **永 (Eternity)**: 해시를 통해 버전을 명확히 추적 가능.

### ✅ SSOT 봉인 규칙 (3원칙)
1. **Truth:** `.excalidraw`가 유일한 소스, `.svg`는 파생 자산으로 함께 커밋.
2. **Sync Rule:** `.svg` 파일 하단 혹은 상단에 `SSOT-SOURCE-SHA256:<sha256(excalidraw)>` 스탬프가 반드시 존재해야 함.
3. **CI Gate:** `verify_visual_sync.py` 검증 실패 시 머지 차단.

---

## 🛠️ 운영 도구

### 1. 스탬프 찍기 (Local)
로컬에서 SVG를 내보낸 후 다음 명령어로 해시를 각인합니다.
```bash
python3 scripts/stamp_visual_ssot.py docs/diagrams
```

### 2. 동기화 검증 (CI)
CI 게이트에서 동기화 여부를 체크합니다.
```bash
python3 scripts/verify_visual_sync.py docs/diagrams
```

---

**Trinity Score (Design)**: 眞 100% | 善 100% | 美 95% | 孝 100% | 永 100%
