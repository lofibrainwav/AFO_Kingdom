"use client";

import React from "react";
import { TrinityGlow } from "./TrinityGlow";

export function RoyalLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen w-full overflow-hidden bg-black text-white">
      <TrinityGlow />
      <div className="relative mx-auto max-w-6xl px-4 py-10">
        <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-2xl">
          <div className="p-6">{children}</div>
        </div>
      </div>
    </div>
  );
}
