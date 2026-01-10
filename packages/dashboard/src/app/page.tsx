"use client";

import { RoyalLayout } from "@/components/royal/RoyalLayout";
import { CouncilOrbits } from "@/components/royal/CouncilOrbits";
import { JulieTaxWidget } from "@/widgets/JulieTaxWidget";
import { useChancellorStream } from "@/hooks/useChancellorStream";

export default function Page() {
  useChancellorStream();

  return (
    <RoyalLayout>
      <div className="text-2xl font-semibold">Digital Royal Palace</div>
      <div className="mt-2 text-sm opacity-70">
        Trinity Glow + Council of Minds + SSE bridge
      </div>
      <CouncilOrbits />
      <JulieTaxWidget />
    </RoyalLayout>
  );
}
