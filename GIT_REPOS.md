# AFO Kingdom - Git 저장소 관리

## 저장소 구조

AFO Kingdom은 3개의 독립적인 Git 저장소로 구성되어 있습니다:

| 저장소 | URL | 역할 |
|--------|-----|------|
| **AFO** | https://github.com/lofibrainwav/AFO.git | 백엔드 (Soul Engine, FastAPI) |
| **TRINITY-OS** | https://github.com/lofibrainwav/TRINITY-OS.git | 오케스트레이션, SSOT 정본 |
| **SixXon** | https://github.com/lofibrainwav/SixXon.git | CLI, Auth, 공개 문서 |

## 디렉토리 구조

```
AFO_Kingdom/              # 로컬 작업 디렉토리 (Git 관리 X)
├── AFO/                  # Git 저장소 1
├── TRINITY-OS/           # Git 저장소 2
├── SixXon/               # Git 저장소 3
├── trinity-dashboard/    # Dashboard (AFO 하위 또는 별도)
├── .cursor/              # Cursor IDE 설정
├── .gemini/              # Antigravity 설정
└── start_kingdom.sh      # 전체 시작 스크립트
```

## 커밋/푸시 워크플로우

### 각 저장소 개별 커밋

```bash
# AFO 저장소
cd AFO_Kingdom/AFO
git add .
git commit -m "feat: 기능 설명"
git push origin main

# TRINITY-OS 저장소
cd AFO_Kingdom/TRINITY-OS
git add .
git commit -m "feat: 기능 설명"
git push origin main

# SixXon 저장소
cd AFO_Kingdom/SixXon
git add .
git commit -m "feat: 기능 설명"
git push origin main
```

### 전체 저장소 상태 확인

```bash
# 모든 저장소 상태 확인
for dir in AFO TRINITY-OS SixXon; do
  echo "=== $dir ==="
  cd /Users/brnestrm/AFO_Kingdom/$dir
  git status --short
  cd ..
done
```

### 전체 저장소 푸시 (주의: 변경 사항 확인 후 사용)

```bash
# 모든 저장소 푸시
for dir in AFO TRINITY-OS SixXon; do
  echo "=== Pushing $dir ==="
  cd /Users/brnestrm/AFO_Kingdom/$dir
  git push origin main
  cd ..
done
```

## 환경변수

모든 설정은 환경변수를 통해 관리됩니다:

```bash
# Soul Engine URL (Dashboard, MCP에서 사용)
export SOUL_ENGINE_URL=http://localhost:8010
```

## 관련 파일

- `.cursor/mcp.json` - Cursor MCP 설정
- `.gemini/settings.json` - Antigravity 설정
- `.gemini/GEMINI.md` - 승상 시스템 프롬프트
- `.cursorrules` - Cursor 시스템 프롬프트
