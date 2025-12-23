import dynamic from "next/dynamic";

/**
 * MermaidDiagram의 지연 로딩 버전
 * 
 * 번들 크기 최적화를 위해 동적 임포트 사용
 */
export const MermaidDiagramLazy = dynamic(
  () => import("./MermaidDiagram").then((mod) => ({ default: mod.MermaidDiagram })),
  {
    loading: () => (
      <div className="p-8 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">다이어그램 로딩 중...</p>
      </div>
    ),
    ssr: false, // 클라이언트 전용 (SSR/하이드레이션 이슈 방지)
  }
);

