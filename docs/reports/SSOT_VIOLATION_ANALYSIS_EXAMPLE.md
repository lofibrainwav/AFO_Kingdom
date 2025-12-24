# SSOT 위반 사례 분석 및 수정 예시

**As-of**: 2025-12-24  
**Status**: SSOT 원칙 위반 사례 분석 (교육용)  
**SSOT 원칙 준수**: 팩트 기반, 과장 제거, 근거 명시

---

## 원본 보고서의 SSOT 위반 사항

### 1. 과장 표현 (100% 사용)

**위반 예시**:
- "진실 100% 확보"
- "선 100% 추구"
- "미 100% 우아한 정리"
- "효 100% 달성"
- "영 100% 이루겠나이다"
- "왕국 PDF 100/100 아키"

**SSOT 원칙**: 모든 수치는 측정 가능한 근거가 있어야 함. "100%"는 완벽함을 의미하므로, 실제로 모든 항목이 완료되었는지 검증 가능해야 함.

**수정 예시**:
- "로컬 배선 완료 상태 확인됨 (localhost:3000 fragments 200 OK, POST /api/revalidate 200 OK)"
- "Vercel 배포 가이드 작성 완료"
- "SSOT 원칙 준수하여 문서 정리 완료"

---

### 2. 할루시네이션 (비존재 자료 언급)

**위반 예시**:
- "첨부된 모든 내용(로컬 배선 완료 상태, Vercel 배포 A/B안, 검증 스크립트, 실패 패턴 4개, 빌더조쉬/된장 정리, 배휘동 리드 실록, 왕국 지혜 4대, GenUI 사례 등 텍스트/이미지/PDF 전체)"
- "왕국 PDF 100/100 아키 + 이미지(시스템 시각화 9 MCP/19 Skills/12 Context7, 전통 궁전 회로판 퓨전, 나침반 개발자 여정, 2025 Developer Ecosystem 슬라이드)"

**SSOT 원칙**: 실제로 존재하는 파일/자료만 언급. 첨부되지 않은 내용은 언급하지 않음.

**수정 예시**:
- "REVALIDATE_URL_SETUP_GUIDE_FACTS_PASTE.md 문서 참조"
- "코드베이스 확인: packages/dashboard/src/app/api/revalidate/route.ts"

---

### 3. 외부 인물 언급 (검증되지 않은 정보)

**위반 예시**:
- "배휘동: Corca AX 팀 활동(2025 Claude Code 밋업 발표), XL8 프론트엔드 팀 리드 3.5년(본인 블로그/LinkedIn)"
- "Builder Josh (Josh Kim): Claude Code 서브 에이전트 관련 인터뷰/활동 확인"
- "커서마피아 (최수민): Cursor AI 바이브 코딩 강의/커뮤니티 활동"

**SSOT 원칙**: 외부 인물의 활동/자료는 실제 링크/출처를 제공해야 함. "확인"이라고만 하면 검증 불가.

**수정 예시**:
- "배휘동: [실제 링크] 참조 (제안)"
- "Builder Josh: [실제 링크] 참조 (제안)"
- 또는 외부 인물 언급 제거

---

### 4. "100/100" 평가 (근거 없는 완벽 평가)

**위반 예시**:
- "왕국 PDF 100/100 아키"
- "진실 100%·선 100%·미 100%·효 100%·영 100% 달성"

**SSOT 원칙**: 평가는 측정 가능한 기준과 근거가 있어야 함. "100/100"은 모든 항목이 완벽함을 의미하므로, 실제로 모든 항목이 완료되었는지 검증 가능해야 함.

**수정 예시**:
- "아키텍처 평가: 기술적 완성도 높음 (제안)"
- "SSOT 원칙 준수하여 문서 작성 완료"

---

### 5. 비존재 자료 언급 (이미지/PDF)

**위반 예시**:
- "이미지(시스템 시각화 9 MCP/19 Skills/12 Context7, 전통 궁전 회로판 퓨전, 나침반 개발자 여정, 2025 Developer Ecosystem 슬라이드)"
- "외부 실시간 자료(Next.js ISR on-demand revalidate 2025 docs, Vercel/GitHub Actions env 설정, 배휘동/Builder Josh/커서마피아 공개 자료, 2025 Developer Ecosystem 보고서 등)"

**SSOT 원칙**: 실제로 존재하는 파일/링크만 언급. 첨부되지 않은 이미지/PDF는 언급하지 않음.

**수정 예시**:
- "Next.js 공식 문서: [링크] 참조"
- "GitHub Actions 공식 문서: [링크] 참조"
- 이미지/PDF 언급 제거 (실제로 첨부되지 않은 경우)

---

## SSOT 준수 버전 (수정 예시)

### ✅ 올바른 SSOT 스타일

**제목**: REVALIDATE_URL 설정 가이드 업데이트 완료

**FACTS (검증됨)**:
- 로컬 배선 완료 상태 확인: `localhost:3000`에서 fragments 200 OK, POST /api/revalidate 200 OK (로컬 로그 기반)
- 코드베이스 확인: `packages/dashboard/src/app/api/revalidate/route.ts` 존재
- Next.js 공식 문서 참조: [링크]

**제안**:
- Vercel 배포 A/B안: B안(vercel.app) 먼저 → A안(brnestrm.com) 순서 추천 (마찰 최소)
- 배포 후 30초 검증 스크립트 제공 (복붙용)

**실패 패턴 4개** (Next.js/Vercel docs 기반):
- 401: Secret 불일치 → Vercel Env / GitHub Secret / 로컬 export 값 3개 동일 확인
- 308/301: URL 리다이렉트 → REVALIDATE_URL 마지막 / 제거
- 403/timeout: WAF/Cloudflare 차단 → Proxy OFF or POST 허용 규칙 추가
- 404: 라우트 미배포 → Vercel 빌드 로그 확인

**참고 자료**:
- [Next.js: revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)
- [GitHub Actions: Using secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Vercel: Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

---

## SSOT 원칙 요약

1. **과장 표현 제거**: "100%", "완벽", "모든" 등은 측정 가능한 근거가 있어야 함
2. **할루시네이션 금지**: 실제로 존재하는 파일/자료만 언급
3. **외부 인물 언급**: 실제 링크/출처 제공 또는 언급 제거
4. **평가 근거**: "100/100" 등은 측정 가능한 기준과 근거 필요
5. **비존재 자료 언급 금지**: 첨부되지 않은 이미지/PDF는 언급하지 않음

---

**참고**: 이 문서는 SSOT 원칙 위반 사례를 교육 목적으로 정리한 것입니다. 실제 보고서 작성 시 위 원칙을 준수해야 합니다.

