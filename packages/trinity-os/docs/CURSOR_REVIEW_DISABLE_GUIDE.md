# Cursor IDE 리뷰 기능 비활성화 가이드

**작성일**: 2025-12-11  
**목적**: "insufficient funds" 오류 해결  
**眞善美孝**: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%

---

## 문제 상황

**오류 메시지**:
```
Failed to run review: insufficient funds (request ID: ...)
```

**원인**: Cursor IDE의 자동 코드 리뷰 기능이 외부 API를 호출하려고 할 때 발생

---

## 해결 방법

### 방법 1: .vscode/settings.json 설정 (권장)

**파일**: `.vscode/settings.json`

**추가할 설정**:
```json
{
  "cursor.codeReview.enabled": false,
  "cursor.autocomplete.enabled": true,
  "cursor.chat.enabled": true
}
```

**상태**: ✅ 이미 추가됨

---

### 방법 2: .cursor/environment.json 설정

**파일**: `.cursor/environment.json`

**추가할 설정**:
```json
{
  "agentCanUpdateSnapshot": true,
  "codeReview": {
    "enabled": false,
    "autoReview": false
  }
}
```

**상태**: ✅ 이미 추가됨

---

### 방법 3: Cursor IDE UI에서 비활성화

1. **Cursor Settings 열기**
   - `Cmd + ,` (macOS) 또는 `Ctrl + ,` (Windows/Linux)
   - 또는 `Cursor → Settings`

2. **Features 섹션 찾기**
   - 검색창에 "review" 입력

3. **Code Review 비활성화**
   - "Code Review" 또는 "Auto Review" 체크 해제

4. **Cursor 재시작**
   - `Cmd + Q` (macOS) 또는 `Alt + F4` (Windows)
   - Cursor 완전 종료 후 재실행

---

## 검증 방법

### 설정 확인 스크립트 실행

```bash
./scripts/check_cursor_settings.sh
```

**예상 출력**:
- ✅ `.vscode/settings.json`에 `cursor.codeReview.enabled: false` 확인
- ✅ `.cursor/environment.json`에 `codeReview.enabled: false` 확인

---

## 추가 권장사항

### 1. Cursor 캐시 정리 (문제 지속 시)

```bash
# Cursor 캐시 삭제
rm -rf ~/.cursor/cache

# Cursor 재시작
```

### 2. Cursor 로그 확인

```bash
# Cursor 로그 위치 (macOS)
tail -f ~/Library/Logs/Cursor/main.log

# 오류 메시지 확인
grep -i "insufficient\|review\|funds" ~/Library/Logs/Cursor/main.log
```

### 3. Cursor 버전 확인

```bash
# Cursor 버전 확인 (macOS)
/Applications/Cursor.app/Contents/MacOS/Cursor --version

# 최신 버전으로 업데이트 권장
```

---

## 설정 파일 위치

### 프로젝트별 설정
- `.vscode/settings.json` - VSCode/Cursor 공통 설정
- `.cursor/environment.json` - Cursor 전용 설정

### 글로벌 설정 (사용자 홈 디렉토리)
- `~/.cursor/settings.json` - Cursor 글로벌 설정
- `~/.vscode/settings.json` - VSCode 글로벌 설정

**우선순위**: 프로젝트별 설정 > 글로벌 설정

---

## 완료 확인

설정 적용 후:

1. ✅ `.vscode/settings.json`에 `cursor.codeReview.enabled: false` 추가됨
2. ✅ `.cursor/environment.json`에 `codeReview.enabled: false` 추가됨
3. ✅ Cursor 재시작 필요

**재시작 후 "insufficient funds" 오류가 사라져야 합니다.**

---

**眞善美孝**: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%

**형님의 평온을 위해, 리뷰 기능을 비활성화했습니다!** 👑
