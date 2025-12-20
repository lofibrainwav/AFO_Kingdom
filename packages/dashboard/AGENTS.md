# 🎨 AFO Dashboard 하위 헌법: AGENTS.md

이 문서는 `dashboard` 영역 내에서 에이전트가 준수해야 할 디자인 및 기술 세부 규칙을 정의합니다.

## 1. 디자인 시스템 (Design System)
*   **Theme**: Sleek Dark Mode & Glassmorphism 필수.
*   **Typography**: Inter 또는 Outfit 폰트 사용.
*   **Animations**: Framer Motion을 사용한 부드러운 전환 효과.

## 2. 기술 표준 (Technical Standards)
*   **Framework**: Next.js 14 (App Router) 필수.
*   **State Management**: SWR (Stale-While-Revalidate)을 통한 데이터 캐싱.
*   **TypeScript**: `any` 타입 사용 금지, 엄격한 인터페이스 정의.

## 3. 에이전트 협업 (Agent Collaboration)
*   프론트엔드 에이전트(`조운`)는 백엔드 에이전트(`관우`)가 제공하는 API 명세를 최우선으로 준수합니다.
