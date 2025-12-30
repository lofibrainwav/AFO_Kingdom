import { RoyalCommandHierarchyCard } from "@/widgets/royal/RoyalCommandHierarchyCard";
import { FieldManualLawCard } from "@/widgets/royal/FieldManualLawCard";
import { HealthWidget } from "@/components/widgets/HealthWidget";
import { SkillsWidget } from "@/components/widgets/SkillsWidget";
import { Context7Widget } from "@/components/widgets/Context7Widget";
import { SyncWidget } from "@/components/widgets/SyncWidget";
import { SystemFingerprintFooter } from "@/components/widgets/SystemFingerprintFooter";

export default function RoyalPage() {
  return (
    <main className="mx-auto w-full max-w-6xl space-y-6 p-6">
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold">Royal Governance</h1>
        <p className="text-sm text-muted-foreground">
          왕국의 지휘 체계와 국법(야전교범)을 대시보드 UI로 고정합니다.
        </p>
      </div>

      {/* Kingdom Intelligence Widgets */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <HealthWidget />
        <SkillsWidget />
        <Context7Widget />
        <SyncWidget />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <RoyalCommandHierarchyCard />
        <FieldManualLawCard />
      </div>

      <SystemFingerprintFooter />
    </main>
  );
}