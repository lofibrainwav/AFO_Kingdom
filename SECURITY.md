# Security Policy - AFO Kingdom

## 眞善美孝永 보안 철학

- **眞 (Truth)**: 취약점 투명 공개
- **善 (Goodness)**: 윤리적 보안 대응
- **美 (Beauty)**: 간결한 보안 프로세스
- **孝 (Serenity)**: 평온한 운영 유지
- **永 (Eternity)**: 장기 보안 유지

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| develop | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

1. **이메일**: 보안 이슈는 공개 Issue 대신 이메일로 제보
2. **응답 시간**: 48시간 내 초기 응답
3. **수정 시간**: Critical은 7일, High는 14일 내 수정

## Security Features

### Automated Scanning (CI)

- **Trivy**: 취약점 + 시크릿 + 설정 오류 스캔
- **Snyk**: Python 의존성 취약점 스캔 + 자동 Fix PR
  - `--severity-threshold=high`: High 이상만 알림
  - `monitor`: main 브랜치 장기 추적
  - 자동 Upgrade PR: 취약 버전 → 안전 버전
- **SARIF**: GitHub Security tab 자동 업로드
- **Codecov**: 테스트 커버리지 추적

### Dependency Management

- **Dependabot**: 자동 보안 업데이트 PR
- **Secret Scanning**: GitHub 기본 활성화 권장

### Code Quality

- **Pyright --standard**: 타입 안전성
- **Ruff**: 코드 품질 린팅
- **pytest-cov**: 테스트 커버리지

## Best Practices

1. API 키는 환경변수로만 관리
2. `.env` 파일 Git에 커밋 금지
3. DRY_RUN 모드로 위험 작업 사전 테스트
4. 모든 외부 입력 Pydantic으로 검증
