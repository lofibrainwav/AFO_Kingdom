import dynamic from "next/dynamic";

/**
 * OrgansMapSVG의 지연 로딩 버전
 * 
 * 번들 크기 최적화를 위해 동적 임포트 사용
 */
export const OrgansMapSVGLazy = dynamic(
  () => import("./OrgansMapSVG").then((mod) => ({ default: mod.OrgansMapSVG })),
  {
    loading: () => (
      <div className="p-8 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">지도 로딩 중...</p>
      </div>
    ),
    ssr: false,
  }
);

