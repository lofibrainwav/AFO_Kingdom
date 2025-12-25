# 🏰 AFO 왕국 프론트엔드 왕궁: AGENTS.md

**Next.js 프론트엔드 규약**

## 기술 스택
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion (애니메이션)

## 실행 명령어
```bash
# 개발 서버
cd packages/dashboard && npm run dev

# 빌드
npm run build

# 타입 체크
npm run type-check

# 린팅
npm run lint
```

## 컴포넌트 설계 원칙
- 함수형 컴포넌트 + Hooks
- TypeScript 엄격 모드
- Tailwind 유틸리티 클래스
- 반응형 디자인 (모바일 우선)

## 상태 관리
- React useState/useEffect (단순 상태)
- Context API (글로벌 상태)
- SWR (서버 상태)

## UI/UX 원칙
- Glassmorphism 디자인
- Trinity Glow 효과
- 접근성 (ARIA 속성)
- 다크 모드 지원

## 배포
- Vercel 자동 배포
- 정적 생성 (SSG)
- CDN 최적화