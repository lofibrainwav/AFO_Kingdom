import React, { useEffect, useState } from 'react';
import { Activity, Shield, Zap } from 'lucide-react';

const RoyalOpsCenter = () => {
  const [kpiData, setKpiData] = useState({
    trinityScore: 98.5,
    serenityStatus: 'High',
    fivePillarsStatus: ['Truth', 'Goodness', 'Beauty', 'Serenity', 'Eternity'],
  });

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate fetching KPI data
      setKpiData((prev) => ({
        ...prev,
        trinityScore: Math.round(prev.trinityScore * (1 + Math.random() - 0.5)),
        serenityStatus: prev.serenityStatus === 'High' ? 'Medium' : 'High',
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const mockSystemEvents = [
    'System Initialized',
    'Grok Connected',
    'Trinity verified',
    'Market volatility detected',
    'Resource allocation update',
  ];

  const getNextEvent = () => {
    const randomIndex = Math.floor(Math.random() * mockSystemEvents.length);
    return mockSystemEvents[randomIndex];
  };

  const [logEvent, setLogEvent] = useState(getNextEvent());

  useEffect(() => {
    const interval = setInterval(() => {
      setLogEvent(getNextEvent());
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-3 h-screen bg-black/40 backdrop-blur-xl">
      {/* Left: Kingdom HUD (KPIs) */}
      <div className="col-span-1 p-8 bg-black/50 border-white/10">
        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-bold">Trinity Score</h2>
          <div className="bg-gradient-to-r from-indigo-700 to-purple-900 text-white p-2 rounded-lg">
            {kpiData.trinityScore.toFixed(1)}
          </div>

          <h2 className="text-lg font-bold">Serenity Status</h2>
          <div
            className={`bg-gradient-to-r ${kpiData.serenityStatus === 'High' ? 'from-green-500 to-green-700' : 'from-red-600 to-red-900'} text-white p-2 rounded-lg`}
          >
            {kpiData.serenityStatus}
          </div>

          <h2 className="text-lg font-bold">Five Pillars Status</h2>
          <ul className="list-disc pl-5">
            {kpiData.fivePillarsStatus.map((pillar, index) => (
              <li key={index} className={`bg-gradient-to-r from-indigo-600 to-purple-800 text-white p-1 rounded-lg`}>
                {pillar}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Center: Chancellor Stream */}
      <div className="col-span-2 p-4 bg-black/50 border-white/10">
        <div className="flex flex-col h-full justify-between">
          <div className="text-lg font-bold mb-2">Chancellor Stream</div>
          <div className="overflow-y-scroll h-[calc(100vh - 6rem)] text-gray-400 font-mono">
            {logEvent}
          </div>
        </div>
      </div>

      {/* Right: Grok Insight Card */}
      <div className="col-span-1 p-8 bg-black/50 border-white/10">
        <div
          className="bg-gradient-to-r from-indigo-600 to-purple-800 text-white p-4 rounded-lg backdrop-blur-xl"
          style={{ backDropFilter: 'blur(10px)' }}
        >
          <h2 className="text-lg font-bold">Grok Insight</h2>
          <div className="mt-2">
            Market volatility detected. Recommend conservative resource allocation.
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoyalOpsCenter;