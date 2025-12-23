import dynamic from "next/dynamic";

/**
 * 위젯들의 지연 로딩 버전
 * 
 * 번들 크기 최적화를 위해 동적 임포트 사용
 */
export const GitWidgetLazy = dynamic(
  () =>
    import("@/components/royal/widgets/GitWidget").then((mod) => ({
      default: mod.GitWidget,
    })),
  {
    loading: () => (
      <div className="p-4 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">위젯 로딩 중...</p>
      </div>
    ),
  }
);

export const SystemStatusWidgetLazy = dynamic(
  () =>
    import("@/components/royal/widgets/SystemStatusWidget").then((mod) => ({
      default: mod.SystemStatusWidget,
    })),
  {
    loading: () => (
      <div className="p-4 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">위젯 로딩 중...</p>
      </div>
    ),
  }
);

export const ProgressTrackerWidgetLazy = dynamic(
  () =>
    import("./ProgressTrackerWidget").then((mod) => ({
      default: mod.ProgressTrackerWidget,
    })),
  {
    loading: () => (
      <div className="p-4 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">위젯 로딩 중...</p>
      </div>
    ),
  }
);

export const OverloadMonitorWidgetLazy = dynamic(
  () =>
    import("./OverloadMonitorWidget").then((mod) => ({
      default: mod.OverloadMonitorWidget,
    })),
  {
    loading: () => (
      <div className="p-4 bg-slate-100 rounded-lg text-center">
        <p className="text-sm text-slate-500">위젯 로딩 중...</p>
      </div>
    ),
  }
);

