# GitHub Actions 보안 가이드

## CVE-2025-30066 교훈 (tj-actions/changed-files)

### 공격 요약

- **기간**: 2025-03-12 ~ 03-15
- **영향**: 23,000+ repos
- **CVSS**: 8.6 (High)
- **벡터**: 태그 이동 → 악성 코드 주입 → secret 로그 노출

### 방어 적용 ✅

| 대책 | AFO Kingdom 상태 |
|------|-----------------|
| SHA Pinning | ✅ 7개 action 모두 |
| Least Privilege | ✅ contents: read |
| Scorecards | ✅ main 브랜치 |
| Trivy/Snyk | ✅ 취약점 스캔 |

---

## OIDC 구현 가이드

### 기본 설정

```yaml
permissions:
  id-token: write  # OIDC 토큰 요청
  contents: read
```

### AWS 예시

```yaml
- uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
  with:
    role-to-assume: arn:aws:iam::123456789:role/GitHubActions
    aws-region: ap-northeast-2
```

### Azure 예시

```yaml
- uses: azure/login@6c251865b4e6290e7b78be643ea2d005bc51f69a
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

### GCP 예시

```yaml
- uses: google-github-actions/auth@6fc4af4b145ae7821d527454aa9bd537d1f2dc5f
  with:
    workload_identity_provider: projects/123/locations/global/workloadIdentityPools/pool/providers/github
    service_account: github-actions@project.iam.gserviceaccount.com
```

---

## Trust Policy (sub claim)

```
repo:ORG/REPO:ref:refs/heads/main      # main 브랜치만
repo:ORG/REPO:environment:production   # prod 환경만
repo:ORG/REPO:pull_request             # PR (주의)
```

---

## 眞善美孝永 보안 매핑

| 기둥 | 보안 조치 |
|------|----------|
| 眞 | SHA pinning, Scorecards |
| 善 | OIDC, least privilege |
| 美 | Reusable workflows |
| 孝 | Harden-runner, auto-update |
| 永 | Secret rotation, audit |
