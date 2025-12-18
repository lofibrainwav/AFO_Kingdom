# SixXon 월구독(웹 로그인) 인증 플로우

목표는 하나입니다.

- **한 번 로그인 → 세션을 Wallet에 암호화 저장 → CLI에서 재사용**

이 플로우는 “API 키 발급”이 아니라, **월구독 웹 세션(브라우저 로그인)**을 SSOT로 삼습니다.

## 원칙(SSOT)

- 세션/토큰/쿠키는 **Git에 커밋하지 않습니다.**
- 진실/상태/근거는 **Receipt(`logs/receipts/<id>/receipt.json` + `raw/*`)**로만 남깁니다.
- SANDBOX에서 `permission_denied`/`docker.sock`/`localhost` 제한은 **DOWN이 아니라 UNKNOWN**으로 기록합니다.

## 브라우저 선택(혼선 제거)

SixXon은 **혼선을 제거하기 위해** 브라우저 엔진을 **`system-chrome` 하나로 고정**합니다.

- `system-chrome`: 설치된 Google Chrome 사용(기본값/왕국 표준)

관련 옵션(현재는 단일 선택만 허용):

- `--browser system-chrome`
- `--keep-open` (열린 브라우저를 유지하며 수동 확인)

## 1) 진단(가볍게)

```bash
./scripts/sixxon auth doctor --json
```

또는(직접 PYTHONPATH 지정):

```bash
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth doctor --json
```

여기서 **`wallet_key_state.key_present=true`**를 먼저 확인합니다.

## 2) 세션 캡처(핵심)

예: Claude

```bash
./scripts/sixxon auth capture --provider claude --browser system-chrome --refresh --json
```

또는:

```bash
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth capture --provider claude --browser system-chrome --refresh --json
```

예: Gemini / Codex / Grok

```bash
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth capture --provider gemini --browser system-chrome --refresh --json
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth capture --provider codex  --browser system-chrome --refresh --json
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth capture --provider grok   --browser system-chrome --refresh --json
```

## 3) 상태 확인(복호화 가능 여부)

```bash
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth status --json
```

- `decryptable=true`면 “지금 환경에서 세션을 정상 사용 가능”입니다.
- `decryptable=false`면 “키/환경이 달라서 복호화 불가”이므로 **재캡처**가 필요합니다.

## 4) 실제 사용(권장: 수동 Open)

웹 UI 변화/Cloudflare 때문에 자동 입력은 깨지기 쉽습니다.
그래서 월구독 플로우의 기본은 **open → 수동 사용**입니다.

```bash
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth open --provider claude --browser system-chrome --keep-open
```

## 5) (옵션) ask 자동 전송(best-effort)

```bash
PYTHONPATH="TRINITY-OS:." python3.12 -m trinity_os.cli.sixxon auth ask --provider claude --yes "3줄로 요약해줘"
```

주의:

- UI/셀렉터/봇 방지로 실패할 수 있습니다.
- 실패하면 Receipt `raw/`에 stdout/stderr/error가 남습니다(SSOT).
