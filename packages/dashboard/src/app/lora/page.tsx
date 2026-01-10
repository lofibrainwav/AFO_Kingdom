"use client";
import { useEffect, useState } from "react";
import { LoRASystemCard } from "../../components/LoRASystemCard";

export default function Page() {
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      // 실시간 SSOT 업데이트 체크 (30초마다)
      setLastUpdate(new Date());
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6">
      <div className="mb-4 text-sm text-gray-600">
        Last SSOT sync: {lastUpdate.toLocaleString()}
      </div>
      <LoRASystemCard />
    </div>
  );
}
